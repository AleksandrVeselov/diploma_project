import requests

from navigation.models import GasStation


# (54.89, 73.51)

def filter_gas_stations(route):
    latitude_list = [route[0] for route in route]
    longitude_list = [route[1] for route in route]
    # gas_stations = GasStation.objects.filter(latitude=54.89, longitude=73.51)
    route_gas_stations = []
    gas_stations = GasStation.objects.all()
    for gas_station in gas_stations:
        for coord1 in gas_station.nearest_road_points:
            for longitude in longitude_list:
                if longitude - 0.001 < coord1[0] < longitude + 0.001:
                    print('true')
                    for latitude in latitude_list:
                        if latitude - 0.001 < coord1[1] < latitude + 0.001:
                            print('true1')
                            route_gas_stations.append(gas_station)
                            break
            break
    return route_gas_stations
