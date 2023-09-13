from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm
from users.models import User

from rest_framework import generics

from users.serializers import UserSerializer


class UserLoginView(LoginView):
    """Контроллер для авторизации"""
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    """Контроллер для выхода пользователя из сервиса"""
    pass


class UserRegisterView(CreateView):
    """Контроллер для регистрации пользователя"""
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'


class UserUpdateView(UpdateView, LoginRequiredMixin):
    """Контроллер для изменения данных пользователя"""
    model = User
    success_url = reverse_lazy('navigation:home')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


def activate_new_user(request, pk):
    """Функция для активации нового пользователя"""
    user = get_user_model()  # получение модели пользователя
    user_for_activate = user.objects.get(id=pk)  # получение пользователя с нужным id
    user_for_activate.is_active = True  # смена флага у пользователя на True
    user_for_activate.save()  # сохранение
    return render(request, 'users/activate.html')


class UserCreateAPIView(generics.CreateAPIView):
    """Создание (регистрация) нового пользователя"""

    serializer_class = UserSerializer
