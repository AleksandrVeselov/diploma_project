from django.contrib import admin

from navigation.models import Route, GasStation, RouteGasStation

admin.site.register(Route)
admin.site.register(GasStation)
admin.site.register(RouteGasStation)
