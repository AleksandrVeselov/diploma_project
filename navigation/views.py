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
from navigation.models import Route, RouteGasStation, RouteCoordinate
from navigation.serializers import RouteSerializer, RouteCoordinateSerializer, RouteGasStationSerializer


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

    def get_form_kwargs(self):
        """Передача в форму request"""

        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

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

    def get_form_kwargs(self):
        """Передача в форму request"""

        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


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

        weather_response = requests.get(weather_url)  # ответ с сайта с погодой
        weather = weather_response.json()['daily']['temperature_2m_max'][0]  # температура

        popup = {'Дизельное топливо': station.price_diesel_fuel,
                 'Погода': weather,
                 'Высота над уровнем моря': station.altitude,
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
        """Добавление информации об авторизованном пользователе"""

        coordinate = form.save()  # сохранение информации о созданной рассылке
        coordinate.owner = self.request.user  # присваиваем атрибуту owner ссылку на текущего пользователя
        coordinate.save()
        return super().form_valid(form)


class RouteListAPIView(generics.ListAPIView):
    """Класс-контроллер для модели Route"""

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


class RouteUpdateAPIView(generics.UpdateAPIView):
    """Класс-контроллер для обновления информации о маршруте"""
    serializer_class = RouteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Фильтрация по пользователю"""
        queryset = Route.objects.filter(owner=self.request.user)
        return queryset


class RouteDestroyAPIView(generics.DestroyAPIView):
    """Класс-контроллер для удаления маршрута Route"""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """фильтрация по пользователю"""

        queryset = Route.objects.filter(owner=self.request.user)

        return queryset


class RouteGasStationsListAPIView(generics.ListAPIView):
    """Просмотр информации о заправках на маршруте"""
    serializer_class = RouteGasStationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self, **kwargs):
        """фильтрация заправок"""

        route_gas_stations = RouteGasStation.objects.filter(route=self.kwargs['pk'])
        queryset = route_gas_stations[0].gas_stations.all()
        return queryset


class CoordinateCreateAPIView(generics.CreateAPIView):
    """класс-контроллер для создания модели Point"""
    permission_classes = [IsAuthenticated]
    serializer_class = RouteCoordinateSerializer

    def perform_create(self, serializer):
        """Добавление пользователя координате"""

        new_coordinate = serializer.save()  # сохранение привычки
        new_coordinate.owner = self.request.user  # добавляем пользователя
        new_coordinate.save()


class CoordinateListAPIView(generics.ListAPIView):
    """класс-представление для вывода списка точек, созданных авторизованным пользователем"""

    serializer_class = RouteCoordinateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """фильтрация маршрутов по текущему пользователю"""

        queryset = RouteCoordinate.objects.filter(owner=self.request.user)

        return queryset






