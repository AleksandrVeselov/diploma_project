import polyline
import requests
from django import forms

from navigation.models import Route


class RouteForm(forms.ModelForm):
    """Форма для создания маршрута"""

    class Meta:
        model = Route
        fields = ('name', 'title', 'start_point', 'end_point')

    def save(self):
        route = super().save()
        print(route)
        route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(route.start_point)};'
                     f'{repr(route.end_point)}?alternatives=true&geometries=polyline&overview=full')

        r = requests.get(route_url)  # отправляем запрос на API для построения маршрута
        res = r.json()
        route.route = res['routes'][0]['geometry']
        route.distance = res['routes'][0]['distance'] / 1000
        route.duration = res['routes'][0]['duration'] / 3600
        return route
