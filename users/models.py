from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""
    username = None

    email = models.EmailField(unique=True, verbose_name='email')

    name = models.CharField(max_length=100, verbose_name='Имя')  # Имя пользователя
    surname = models.CharField(max_length=100, verbose_name='Фамилия')  # Фамилия пользователя
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
