from django.conf import settings
from django.db import models

NULLABLE = {'null': True, 'blank': True}  # для необязательного поля


class RouteCoordinate(models.Model):
    """Модель координаты для маршрута"""

    title = models.TextField(verbose_name='Название точки')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота')

    class Meta:
        verbose_name = 'Координата'
        verbose_name_plural = 'Координаты'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'{self.longitude},{self.latitude}'


class GasStation(models.Model):
    """Модель заправка"""
    price_diesel_fuel = models.DecimalField(max_digits=5, decimal_places=1, verbose_name='Стоимость дизельного топлива')
    altitude = models.IntegerField(verbose_name='Высота над уровнем моря')
    latitude = models.DecimalField(max_digits=9, decimal_places=5, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=5, verbose_name='Долгота')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        verbose_name = 'Заправка'
        verbose_name_plural = 'Заправки'

    def __str__(self):
        return f'({self.latitude}, {self.longitude})'


class Route(models.Model):
    """Модель маршрута"""

    name = models.CharField(max_length=155, verbose_name='Название маршрута')
    title = models.TextField(verbose_name='Описание маршрута')
    duration = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Общее время', **NULLABLE)
    distance = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Общая дистанция', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE,
                              verbose_name='пользователь', **NULLABLE)
    start_point = models.ForeignKey(RouteCoordinate, on_delete=models.CASCADE,
                                    verbose_name='Начальная точка',
                                    related_name='start_point')
    end_point = models.ForeignKey(RouteCoordinate, on_delete=models.CASCADE,
                                  verbose_name='Конечная точка',
                                  related_name='end_point')
    middle_point1 = models.ForeignKey(RouteCoordinate,
                                          verbose_name='Промежуточная координата1',
                                          **NULLABLE,
                                          related_name='middle_point1',
                                          on_delete=models.SET_NULL)
    middle_point2 = models.ForeignKey(RouteCoordinate,
                                      verbose_name='Промежуточная координата2',
                                      **NULLABLE,
                                      related_name='middle_point2',
                                      on_delete=models.SET_NULL)
    middle_point3 = models.ForeignKey(RouteCoordinate,
                                      verbose_name='Промежуточная координата3',
                                      **NULLABLE,
                                      related_name='middle_point3',
                                      on_delete=models.SET_NULL)
    route = models.JSONField(**NULLABLE, verbose_name='Координаты маршрута')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return self.name


class RouteGasStation(models.Model):
    """Заправки на маршруте"""

    route = models.OneToOneField(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    gas_stations = models.ManyToManyField(GasStation, verbose_name='Заправки')
    