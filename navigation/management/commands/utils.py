import requests

from navigation.models import GasStation


def filter_gas_stations(route):
    # gas_stations = GasStation.objects.filter(latitude=54.89, longitude=73.51)
    route_gas_stations = []
    gas_stations = GasStation.objects.all()
    for gas_station in gas_stations:
        for coord in gas_station.nearest_road_points:
            for coord1 in route:
                if coord1[1] - 0.03 < coord[0] < coord1[1] + 0.03:
                    print('true')
                    if coord1[0] - 0.03 < coord[1] < coord1[0] + 0.03:
                        print('true1')
                        route_gas_stations.append(gas_station)
                        break

            break
    print(len(route_gas_stations))
    return route_gas_stations
