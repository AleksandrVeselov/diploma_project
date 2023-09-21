import polyline
import requests

from navigation.models import GasStation, RouteGasStation


def filter_gas_stations(route):
    """
    Функция для фильтрации заправок по маршруту
    """

    decode_route = polyline.decode(route)  # декодирование маршрута
    route_gas_stations = []  # список заправок на маршруте
    gas_stations = GasStation.objects.all()  # заправки из базы данных

    for gas_station in gas_stations:
        for coord in decode_route:

            # если долгота заправки входит в диапазон
            if coord[1] - 0.03 < gas_station.longitude < coord[1] + 0.03:

                # если широта заправки входит в диапазон, значит она находится где-то рядом с точкой на маршруте
                if coord[0] - 0.03 < gas_station.latitude < coord[0] + 0.03:

                    altitude = get_altitude(gas_station) # запрашиваем от api ее высоту
                    gas_station.altitude = altitude  # присваиваем атрибуту altitude
                    gas_station.save()  # сохраняем
                    route_gas_stations.append(gas_station)  # добавляем в список заправок на маршруте
                    break

    return route_gas_stations


def get_altitude(station):
    """
    Функция для вычисления по координатам высоты над уровнем моря
    """

    # url для получения высоты точки над уровнем моря
    elevation_url = (f'https://api.open-meteo.com/v1/elevation?latitude={station.latitude}&'
                     f'longitude={station.longitude}')

    elevation_response = requests.get(elevation_url)  # ответ с сайта с высотой над уровнем моря
    elevation = elevation_response.json()['elevation'][0]  # высота над уровнем моря
    return elevation


def get_route(start_point: float, end_point: float, *points):
    """
    Функция для отправки запроса на сервис построения маршрутов http://project-osrm.org
    start_point: начальная точка маршрута
    end_point: конечная точка маршрута
    points: промежуточные точки на маршруте
    """

    # если промежуточные точки есть
    if points:
        coordinates = ';'.join([repr(point) for point in points])  # собираем точки в строку

        # формируем url для отправки запроса на сервер построения маршрутов
        route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(start_point)};'
                     f'{coordinates};{repr(end_point)}?alternatives=true&geometries=polyline&overview=full')

    # если промежуточных точек нет
    else:
        # формируем url для отправки запроса на сервер построения маршрутов
        route_url = (f'http://router.project-osrm.org/route/v1/driving/{repr(start_point)};'
                     f'{repr(end_point)}?alternatives=true&geometries=polyline&overview=full')
    request = requests.get(route_url)  # отправляем запрос на сервер для построения маршрута
    if request.status_code == 200:
        res = request.json()  # ответ с сервера в формате json

    return res