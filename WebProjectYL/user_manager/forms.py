from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={

            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ), label='Пароль')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'status', 'birth_date')
