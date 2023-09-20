from rest_framework import serializers

from navigation.management.commands.utils import get_route, filter_gas_stations
from navigation.models import Route, RouteCoordinate, RouteGasStation, GasStation


class RouteSerializer(serializers.ModelSerializer):
    """Сериализатор модели маршрут"""

    class Meta:
        model = Route
        exclude = ['route']

    def save(self, **kwargs):
        new_route = super().save(**kwargs)
        points = filter(lambda x: x is not None,
                        [new_route.middle_point1, new_route.middle_point2, new_route.middle_point3])
        if points:
            new_route_geometry = get_route(new_route.start_point, new_route.end_point, *points)
        else:
            new_route_geometry = get_route(new_route.start_point, new_route.end_point)
        new_route.route = new_route_geometry['routes'][0]['geometry']  # сохраняем в базе данных геометрию маршрута

        # сохраняем в базе данных геометрию дистанцию маршрута, переведенную в километры
        new_route.distance = new_route_geometry['routes'][0]['distance'] / 1000
        # сохраняем в базе данных длительность маршрута, переведенную в часы
        new_route.duration = new_route_geometry['routes'][0]['duration'] / 3600
        gas_stations_on_route = filter_gas_stations(new_route.route)  # получаем заправки на маршруте

        # проверяем есть ли в базе данных заправки на маршруте по id
        route_gas_station_model = RouteGasStation.objects.filter(route=new_route)

        # если пришел пустой список, создаем экземпляр класса RouteGasStation и записываем в него заправки
        if not route_gas_station_model:
            route_gas_station_model = RouteGasStation.objects.create(route=new_route)
            route_gas_station_model.gas_stations.set(gas_stations_on_route)

        # иначе обновляем заправки на маршруте
        else:
            route_gas_station_model[0].gas_stations.set(gas_stations_on_route)
        new_route.owner = self.context['request'].user  # присваиваем маршруту пользователя
        new_route.save()  # сохраняем изменения
        return new_route


class RouteCoordinateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteCoordinate
        fields = '__all__'


class RouteGasStationSerializer(serializers.ModelSerializer):

    class Meta:
        model = GasStation
        fields = '__all__'

