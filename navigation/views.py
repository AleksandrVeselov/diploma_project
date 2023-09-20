import folium
import polyline
import requests
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from navigation.forms import RouteForm, CoordinateForm
from navigation.management.commands.utils import filter_gas_stations
from navigation.models import Route, RouteGasStation, RouteCoordinate
from navigation.serializers import RouteSerializer


def home(request):
    """Контроллер главной страницы"""

    if request.user:
        routes_list = Route.objects.filter(owner=request.user.id)  # список всех маршрутов текущего пользователя
    else:
        routes_list = []

    context = {
        'object_list': routes_list,
    }

    return render(request, 'navigation/homepage.html', context)


class RouteGasStationView(TemplateView, LoginRequiredMixin):
    """Класс-контроллер для отображения списка АЗС на маршруте"""

    template_name = 'navigation/routegasstation_list.html'  # файл шаблона

    def get_context_data(self, **kwargs):
        """передача в контекст списка с АЗС на маршруте"""

        context = super().get_context_data(**kwargs)
        route_gas_stations = RouteGasStation.objects.get(route=self.kwargs.get('pk'))
        context['route_gas_stations'] = route_gas_stations
        return context


class RouteCreateView(CreateView, LoginRequiredMixin):
    """Класс-контроллер для создания маршрута"""

    model = Route
    form_class = RouteForm
    success_url = reverse_lazy('navigation:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        route = form.save()  # сохранение информации о созданном маршруте
        route.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        route.save()
        return super().form_valid(form)


class RouteUpdateView(UpdateView, LoginRequiredMixin):
    """Класс-контроллер для обновления маршрута"""

    model = Route  # модель
    form_class = RouteForm  # форма
    success_url = reverse_lazy('navigation:home')  # адрес для перенаправления

    def form_valid(self, form):
        form.save()  # сохранение информации о созданном маршруте
        return super().form_valid(form)


@login_required
def showmap(request, pk):
    """Контроллер для отображения карты на странице"""
    route = Route.objects.get(pk=pk)  # получаем маршрут по его id

    decode_route = polyline.decode(route.route)  # декодируем геометрию для получение координат на маршруте

    russia_map = folium.Map(
        location=[64.6863136, 97.7453061],  # широта и долгота России
        zoom_start=4  # масштаб карты
    )  # получаем карту России

    figure = folium.Figure()

    folium.PolyLine(decode_route, weight=8, color='blue', opacity=0.6).add_to(russia_map)  # рисуем на карте маршрут
    gas_stations_on_route = RouteGasStation.objects.get(route=route)  # получаем заправки на маршруте

    # цикл для отображения заправок на карте
    for station in gas_stations_on_route.gas_stations.all():

        # url для получения погоды по координатам
        weather_url = (f'https://api.open-meteo.com/v1/forecast?latitude={station.latitude}&'
                       f'longitude={station.longitude}&daily=temperature_2m_max&forecast_days=1')

        # url для получения высоты точки над уровнем моря
        elevation_url = (f'https://api.open-meteo.com/v1/elevation?latitude={station.latitude}&'
                         f'longitude={station.longitude}')

        weather_response = requests.get(weather_url)  # ответ с сайта с погодой
        elevation_response = requests.get(elevation_url)  # ответ с сайта с высотой над уровнем моря
        weather = weather_response.json()['daily']['temperature_2m_max'][0]  # температура
        elevation = elevation_response.json()['elevation']  # высота над уровнем моря

        popup = {'Дизельное топливо': station.price_diesel_fuel,
                 'Погода': weather,
                 'Высота над уровнем моря': elevation,
                 'Адрес': station.address,
                 'Координаты': str(station),
                 }  # заметка на маркере АЗС на карте

        folium.Marker(location=(station.latitude, station.longitude),
                      icon=folium.Icon(icon='play', color='green'),
                      popup=popup).add_to(russia_map)  # добаляем на карту маркер АЗС

    figure.render()  # отрисовываем карту

    map = russia_map._repr_html_()  # получаем код страницы для передачи в шаблон

    context = {'map': map}
    return render(request, 'navigation/map.html', context)


class RouteDeleteView(DeleteView, LoginRequiredMixin):
    model = Route
    success_url = reverse_lazy('navigation:home')


class RouteCoordinateCreateView(CreateView, LoginRequiredMixin):
    model = RouteCoordinate
    form_class = CoordinateForm
    success_url = reverse_lazy('navigation:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        route = form.save()  # сохранение информации о созданной рассылке
        route.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        route.save()
        return super().form_valid(form)


class RouteListAPIView(generics.ListAPIView):
    """Класс-контроллер для модели Route на основе """

    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """фильтрация маршрутов по текущему пользователю"""

        queryset = Route.objects.filter(owner=self.request.user)

        return queryset


class RouteCreateAPIView(generics.CreateAPIView):
    """Класс-контроллер для создания экземпляра класса Route"""
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):

        new_route = serializer.save()

        points = list(filter(lambda x: x is not None,
                        [new_route.middle_point1, new_route.middle_point2, new_route.middle_point3]))

        # если промежуточные точки есть
        if points:
            coordinates = ';'.join([repr(point) for point in points])  # собираем точки в строку

            # формируем url для отправки запроса на сервер построения маршрутов
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(new_route.start_point)};'
                         f'{coordinates};{repr(new_route.end_point)}?alternatives=true&geometries=polyline&overview=full')

        # если промежуточных точек нет
        else:
            # формируем url для отправки запроса на сервер построения маршрутов
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(new_route.start_point)};'
                         f'{repr(new_route.end_point)}?alternatives=true&geometries=polyline&overview=full')
        request = requests.get(route_url)  # отправляем запрос на сервер для построения маршрута
        if request.status_code == 200:
            res = request.json()  # ответ с сервера в формате json
            new_route.route = res['routes'][0]['geometry']  # сохранем в базе данных геометрию маршрута

            # сохраняем в базе данных геометрию дистанцию маршрута, переведенную в километры
            new_route.distance = res['routes'][0]['distance'] / 1000
            # сохраняем в базе данных длительность маршрута, переведенную в часы
            new_route.duration = res['routes'][0]['duration'] / 3600
            gas_stations_on_route = filter_gas_stations(new_route.route)  # получаем заправки на маршруте

            # проверяем есть ли в базе данных заправки на маршруте по id
            route_gas_station_model = RouteGasStation.objects.filter(route=new_route)

            # если пришел путсой список, создаем экземпляр класса RouteGasStation и записываем в него заправки
            if not route_gas_station_model:
                route_gas_station_model = RouteGasStation.objects.create(route=new_route)
                route_gas_station_model.gas_stations.set(gas_stations_on_route)

            # иначе обновляем заправки на маршруте
            else:
                route_gas_station_model[0].gas_stations.set(gas_stations_on_route)
            new_route.owner = self.request.user
            new_route.save()


class RouteUpdateApiView(generics.UpdateAPIView):
    """Класс-контроллер для обновления информации о маршруте"""
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):





