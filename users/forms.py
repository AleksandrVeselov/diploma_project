from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.mail import send_mail

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password1', 'password2')
        template_name = 'users/register.html'

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('name', 'surname')

    def __init__(self, *args, **kwargs):
        """Стилизация формы"""
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['password'].widget = forms.HiddenInput()
