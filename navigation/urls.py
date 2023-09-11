from django.urls import path

from navigation.apps import NavigationConfig
from navigation.views import home

app_name = NavigationConfig.name

urlpatterns = [
    path('', home, name='home'),  # главная страница (http://127.0.0.1:8000/)
]