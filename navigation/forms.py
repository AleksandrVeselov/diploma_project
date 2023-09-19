import requests
from django import forms

from navigation.management.commands.utils import filter_gas_stations
from navigation.models import Route, RouteCoordinate, RouteGasStation


class RouteForm(forms.ModelForm):
    """Форма для создания маршрута"""

    class Meta:
        model = Route
        fields = ('name', 'title', 'start_point', 'end_point', 'middle_point1', 'middle_point2', 'middle_point3')

    def save(self):
        """Сохранение информации о созданном маршруте"""

        route = super().save()

        # промежуточные точки на маршруте
        points = list(filter(lambda x: x is not None,
                        [route.middle_point1, route.middle_point2, route.middle_point3]))

        # если промежуточные точки есть
        if points:
            coordinates = ';'.join([repr(point) for point in points])  # собираем точки в строку

            # формируем url для отправки запроса на сервер построения маршрутов
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(route.start_point)};'
                         f'{coordinates};{repr(route.end_point)}?alternatives=true&geometries=polyline&overview=full')

        # если промежуточных точек нет
        else:
            # формируем url для отправки запроса на сервер построения маршрутов
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(route.start_point)};'
                         f'{repr(route.end_point)}?alternatives=true&geometries=polyline&overview=full')
        request = requests.get(route_url)  # отправляем запрос на сервер для построения маршрута
        if request.status_code == 200:
            res = request.json()  # ответ с сервера в формате json
            route.route = res['routes'][0]['geometry']  # сохранем в базе данных геометрию маршрута

            # сохраняем в базе данных геометрию дистанцию маршрута, переведенную в километры
            route.distance = res['routes'][0]['distance'] / 1000
            # сохраняем в базе данных длительность маршрута, переведенную в часы
            route.duration = res['routes'][0]['duration'] / 3600

            gas_stations_on_route = filter_gas_stations(route.route)
            route_gas_station_model = RouteGasStation.objects.filter(route=route)
            if not route_gas_station_model:
                route_gas_station_model = RouteGasStation.objects.create(route=route)
                route_gas_station_model.gas_stations.set(gas_stations_on_route)
            else:
                route_gas_station_model[0].gas_stations.set(gas_stations_on_route)
        return route


class CoordinateForm(forms.ModelForm):
    class Meta:
        model = RouteCoordinate
        fields = ('title', 'latitude', 'longitude')
