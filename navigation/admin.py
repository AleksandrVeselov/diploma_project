from django.contrib import admin

from navigation.models import Route, GasStation, RouteGasStation, RouteCoordinate

admin.site.register(Route)
admin.site.register(GasStation)
admin.site.register(RouteGasStation)
admin.site.register(RouteCoordinate)
