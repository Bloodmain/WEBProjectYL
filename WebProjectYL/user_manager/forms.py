from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, News
import datetime as dt

from django import forms


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин', 'id': 'username'}), required=True,
        label='')
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'password',
        }
    ), label='', required=True)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Логин', 'id': 'username'}),
        label='', required=True)
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'id': 'password',
        }
    ), label='', required=True)
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Адрес электронной почты', 'id': 'email'}),
        label='', required=True)
    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Имя', 'id': 'first-name'}),
        label='', required=True)
    last_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Фамилия', 'id': 'last-name'}),
        label='', required=True)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'status', 'birth_date', 'avatar')

    birth_date = forms.DateField(widget=forms.DateInput(
        attrs={
            'class': 'form-control bd',
            'placeholder': 'Дата рождения',
            'id': 'birthdate',
        },
    ), label='', required=True)

    status = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Статус', 'id': 'status'}),
        label='', required=False)

    bio = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'О себе', 'id': 'bio'}),
        label='', required=False)

    avatar = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control avatar', 'placeholder': ''}),
        label='', required=False)


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('text_content',)

    text_content = forms.CharField(widget=forms.Textarea(
        attrs={'class': 'news_input', 'placeholder': 'Создайте новость...'}),
        label='', required=True)

    attachments = forms.FileField(
        widget=forms.ClearableFileInput(
            attrs={'multiple': True, 'class': 'news_files'}),
        label='', required=False)
