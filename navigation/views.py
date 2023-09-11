from django.shortcuts import render
from django.views.generic import ListView

from navigation.models import Route


def home(request):
    """Контроллер главной страницы"""

    routes_list = Route.objects.all()  # список всех маршрутов

    context = {
        'object_list': routes_list
    }

    return render(request, 'navigation/homepage.html', context)

