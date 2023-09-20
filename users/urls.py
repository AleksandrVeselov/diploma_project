from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import path, reverse_lazy
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserLoginView, UserLogoutView, UserRegisterView, UserUpdateView, activate_new_user, \
    UserCreateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),  # авторизация пользователя
    path('logout/', UserLogoutView.as_view(), name='logout'),  # выход из системы
    path('register/', UserRegisterView.as_view(), name='register'),  # регистрация пользователя
    path('profile/', UserUpdateView.as_view(), name='profile'),  # изменения данных пользователя
    path('activate/<int:pk>/', activate_new_user, name='activate'),  # активация пользователя
    path('password_change/', PasswordChangeView.as_view(template_name='users/password_change_form.html',
                                                        success_url=reverse_lazy('users:password_change_done')),
         name='change_password'),  # смена пароля
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),
         name='password_change_done'),  # страница успешной смены пароля
    path('api/register/', UserCreateAPIView.as_view(), name='user_create'),  # регистрация пользователя через api
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # запрос на получение токена
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')  # запрос на обновление токена
]
