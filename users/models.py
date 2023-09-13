from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    username = models.CharField(max_length=32, blank=True, null=True)

    email = models.EmailField(unique=True, verbose_name='email')

    name = models.CharField(max_length=100, verbose_name='Имя')  # Имя пользователя
    surname = models.CharField(max_length=100, verbose_name='Фамилия')  # Фамилия пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.name} {self.surname}'

    def save(self, *args, **kwargs):

        super().save()  # сохраение в переменной пользователя
        send_mail(subject='Активация',
                  message=f'Для активации профиля пройдите по ссылке - http://127.0.0.1:8000/users/activate/{self.pk}/',
                  from_email=settings.EMAIL_HOST_USER,
                  recipient_list=[self.email])  # отправка письма на почту
        self.is_active = False  # смена флага на неактивный

