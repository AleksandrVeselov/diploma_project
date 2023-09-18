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
    route = Route.objects.get(pk=pk)
    decode_route = polyline.decode(route.route)

    russia_map = folium.Map(
        location=[64.6863136, 97.7453061],  # широта и долгота России
        zoom_start=4
    )

    figure = folium.Figure()
    folium.PolyLine(decode_route, weight=8, color='blue', opacity=0.6).add_to(russia_map)
    route_gas_stations = filter_gas_stations(decode_route)
    for station in route_gas_stations:
        # weather_url = (f'https://api.open-meteo.com/v1/forecast?latitude={station.latitude}&longitude={station.longitude}'
        #                f'&daily=temperature_2m_max&forecast_days=1')
        # response = requests.get(weather_url)
        # weather = response.json()['daily']['temperature_2m_max'][0]

        popup = {'Дизельное топливо': station.price_diesel_fuel,
                 'Погода': 'weather',
                 'Высота над уровнем моря': station.altitude,
                 'Адрес': station.address,
                 'Координаты': str(station),
                 }

        folium.Marker(location=(station.latitude, station.longitude),
                      icon=folium.Icon(icon='play', color='green'),
                      popup=popup).add_to(russia_map)

    figure.render()
    map = russia_map._repr_html_()
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






