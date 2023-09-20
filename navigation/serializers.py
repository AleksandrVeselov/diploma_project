from rest_framework import serializers

from navigation.models import Route, RouteCoordinate


class RouteSerializer(serializers.ModelSerializer):
    """Сериализатор модели маршрут"""

    class Meta:
        model = Route
        exclude = ['route']


class RouteCoordinateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RouteCoordinate
        fields = '__all__'
