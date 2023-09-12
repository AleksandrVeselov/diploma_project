from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.template.context_processors import csrf
from django.views.generic import ListView

from navigation.models import Route


def home(request):
    """Контроллер главной страницы"""

    routes_list = Route.objects.all()  # список всех маршрутов

    context = {
        'object_list': routes_list,
    }

    return render(request, 'navigation/homepage.html', context)


