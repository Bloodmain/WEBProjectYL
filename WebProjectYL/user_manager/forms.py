from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile
import datetime as dt

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ), label='Пароль', required=True)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'username'}),
        label='Имя пользователя', required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'password',
        }
    ), label='Пароль', required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'email'}),
        label='Адрес электронной почты', required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'first-name'}),
        label='Имя', required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'last-name'}),
        label='Фамилия', required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'avatar', 'status', 'birth_date')

    birth_date = forms.DateField(widget=forms.SelectDateWidget(
        attrs={
            'class': 'form-control',
            'placeholder': '',
            'id': 'birthdate',
        },
        years=list(range(1950, dt.date.today().year + 1))
    ), label='Дата рождения', required=True)

    status = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'status'}),
        label='Статус', required=False)

    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'bio'}),
        label='О себе', required=False)

    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'placeholder': '', 'id': 'avatar'}),
        label='Аватар', required=False)
