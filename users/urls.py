from django.urls import path

from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, UserUpdateView, activate_new_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # авторизация пользователя
    path('logout/', UserLogoutView.as_view(), name='logout'),  # выход из системы
    path('register/', UserRegisterView.as_view(), name='register'),  # регистрация пользователя
    path('profile/', UserUpdateView.as_view(), name='profile'),  # изменения данных пользователя
    path('activate/<int:pk>/', activate_new_user, name='activate'),  # активация пользователя
]