from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class Route(models.Model):
    """Модель маршрута"""

    start_point = models.CharField(max_length=155, verbose_name='Начальная точка')
    end_point = models.CharField(max_length=155, verbose_name='Конечная точка')
    time = models.DurationField(verbose_name='Общее время')
    distance = models.IntegerField(verbose_name='Общая дистанция')
    link_to_route = models.CharField(max_length=255, verbose_name='Ссылка на маршрут')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                              verbose_name='пользователь', **NULLABLE)

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'{self.start_point}-{self.end_point}'


class GasStation(models.Model):
    """Модель заправка"""
    price_diesel_fuel = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Стоимость дизельного топлива')
    altitude = models.IntegerField(verbose_name='Высота над уровнем моря')
    width = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Долгота')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        verbose_name = 'Заправка'
        verbose_name_plural = 'Заправки'

    def __str__(self):
        return f'Координаты - широта: {self.width}, долгота: {self.longitude}'


class RouteGasStation(models.Model):
    """Заправки на маршруте"""

    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    gas_stations = models.ManyToManyField(GasStation, verbose_name='Заправки')
    