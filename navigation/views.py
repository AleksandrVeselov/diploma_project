from django.shortcuts import render
from navigation.models import Route


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


