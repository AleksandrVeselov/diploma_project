from django.shortcuts import render
from django.views.generic import ListView

from navigation.models import Route, GasStation


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
    model = GasStation



