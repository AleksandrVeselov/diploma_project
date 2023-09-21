from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from navigation.management.commands.fill import Command
from navigation.models import RouteCoordinate, Route
from users.models import User


# Create your tests here.

class RouteTestCase(APITestCase):

    def setUp(self):
        """Подготовка данных перед каждым тестом"""

        # Создание пользователя для тестирования
        self.user = User.objects.create(email='test_user@test.ru',
                                        is_staff=False,
                                        is_superuser=False,
                                        is_active=True)

        self.user.set_password('qwerty')  # Устанавливаем пароль
        self.user.save()  # Сохраняем изменения пользователя в базе данных

        # Запрос токена для авторизации
        response = self.client.post('/users/api/token/', data={'email': self.user.email, 'password': 'qwerty'})

        self.access_token = response.data.get('access')  # Токен для авторизации

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)  # Авторизация пользователя

        self.coordinate1 = RouteCoordinate.objects.create(title='Владимир', latitude=56.129057, longitude=40.406635)
        self.coordinate2 = RouteCoordinate.objects.create(title='Москва', latitude=55.755864, longitude=37.617698)


    def test_create_coordinate(self):

        data = {
            'title': 'Санкт-Петербург',
            'latitude': 59.938784,
            'longitude': 30.314997
        }

        response = self.client.post(reverse('navigation:point_api_create'), data=data)  # отправка запроса

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # проверяем статус ответа

        self.assertEqual(RouteCoordinate.objects.all().count(), 3)  # проверяем наличия в базе данных новой записи

    def test_list_points(self):

        response = self.client.get(reverse('navigation:point_api_list'))  # Запрос на получение списка привычек

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Проверка ответа на запрос

    def test_create_route(self):
        data = {
            'name': 'test',
            'title': 'test',
            'start_point': self.coordinate1.pk,
            'end_point': self.coordinate2.pk
        }
        response = self.client.post(reverse('navigation:route_api_create'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # Проверка ответа на запрос
        self.assertEqual(response.json()['duration'], '2.66')
        self.assertEqual(response.json()['distance'], '200.32')


