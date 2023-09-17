import requests
from django import forms

from navigation.models import Route, RouteCoordinate


class RouteForm(forms.ModelForm):
    """Форма для создания маршрута"""

    class Meta:
        model = Route
        fields = ('name', 'title', 'start_point', 'end_point', 'middle_point1', 'middle_point2', 'middle_point3')

    def save(self):

        route = super().save()
        points = filter(lambda x: x is not None,
                        [route.middle_point1, route.middle_point2, route.middle_point3])
        coordinates = ';'.join([repr(point) for point in points])

        if points:
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(route.start_point)};'
                         f'{coordinates};{repr(route.end_point)}?alternatives=true&geometries=polyline&overview=full')
        else:
            route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(route.start_point)};'
                         
                         f'{repr(route.end_point)}?alternatives=true&geometries=polyline&overview=full')
        r = requests.get(route_url)  # отправляем запрос на API для построения маршрута
        res = r.json()
        route.route = res['routes'][0]['geometry']
        route.distance = res['routes'][0]['distance'] / 1000
        route.duration = res['routes'][0]['duration'] / 3600
        return route


class CoordinateForm(forms.ModelForm):
    class Meta:
        model = RouteCoordinate
        fields = ('title', 'latitude', 'longitude')
