import folium
import polyline
import requests
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from navigation.forms import RouteForm, CoordinateForm
from navigation.management.commands.utils import filter_gas_stations
from navigation.models import Route, RouteGasStation, GasStation, RouteCoordinate


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


class GasStationListView(ListView):
    """Класс-контроллер для отображения списка АЗС на маршруте"""
    model = Route

    def get_queryset(self, *args, **kwargs):
        route_gas_stations = RouteGasStation.objects.filter(route=self.kwargs.get('pk'))
        return route_gas_stations


class RouteCreateView(CreateView):
    model = Route
    form_class = RouteForm
    success_url = reverse_lazy('navigation:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        route = form.save()  # сохранение информации о созданной рассылке
        route.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        route.save()
        return super().form_valid(form)


class RouteUpdateView(UpdateView):
    model = Route
    form_class = RouteForm
    success_url = reverse_lazy('navigation:home')

    def form_valid(self, form):

        form.save()  # сохранение информации о созданной рассылке
        print('save')
        return super().form_valid(form)


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

        elevation_url = (f'https://api.open-meteo.com/v1/elevation?latitude={station.latitude}&'
                       f'longitude={station.longitude}')

        weather_response = requests.get(weather_url)  # ответ с сайта
        elevation_response = requests.get(elevation_url)  # ответ с сайта
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


class RouteDeleteView(DeleteView):
    model = Route
    success_url = reverse_lazy('navigation:home')


class RouteCoordinateCreateView(CreateView):
    model = RouteCoordinate
    form_class = CoordinateForm
    success_url = reverse_lazy('navigation:home')

    def form_valid(self, form):
        """Добавление в создаваемый продукт информации об авторизованном пользователе"""

        route = form.save()  # сохранение информации о созданной рассылке
        route.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        route.save()
        return super().form_valid(form)






