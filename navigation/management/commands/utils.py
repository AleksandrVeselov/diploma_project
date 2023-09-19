import polyline
import requests

from navigation.models import GasStation, RouteGasStation


def filter_gas_stations(route):
    decode_route = polyline.decode(route)
    route_gas_stations = []
    gas_stations = GasStation.objects.all()
    for gas_station in gas_stations:
        for coord in decode_route:
            if coord[1] - 0.03 < gas_station.longitude < coord[1] + 0.03:
                if coord[0] - 0.03 < gas_station.latitude < coord[0] + 0.03:
                    route_gas_stations.append(gas_station)
                    break
    return route_gas_stations
