from django.urls import path

from navigation.apps import NavigationConfig
from navigation.views import (home, RouteGasStationView, RouteCreateView, showmap, RouteUpdateView, RouteDeleteView,
                              RouteCoordinateCreateView, RouteListAPIView, RouteCreateAPIView, RouteUpdateAPIView)

app_name = NavigationConfig.name

urlpatterns = [
    path('', home, name='home'),  # главная страница (http://127.0.0.1:8000/)
    path('route/<int:pk>/gas-stations', RouteGasStationView.as_view(), name='gas-stations'),
    path('route/create', RouteCreateView.as_view(), name='route_create'),
    path('route/map/<int:pk>', showmap, name='route_map'),
    path('route/update/<int:pk>', RouteUpdateView.as_view(), name='route_update'),
    path('route/delete/<int:pk>', RouteDeleteView.as_view(), name='route_delete'),
    path('point/create', RouteCoordinateCreateView.as_view(), name='point_create'),
    path('api/route/', RouteListAPIView.as_view(), name='route_api_list'),
    path('api/route/create/', RouteCreateAPIView.as_view(), name='route_api_create'),
    path('api/route/update/<int:pk>', RouteUpdateAPIView.as_view(), name='route_api_update')
]