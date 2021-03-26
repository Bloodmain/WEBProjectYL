from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserLoginForm, UserForm, ProfileForm
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request):
        return render(request, self.template_name, {})


class LoginView(FormView):
    form_class = UserLoginForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            user.profile.name = user_form.cleaned_data['first_name']
            user.profile.surname = user_form.cleaned_data['last_name']
            user.profile.bio = profile_form.cleaned_data['bio']
            user.profile.status = profile_form.cleaned_data['status']
            user.profile.avatar = profile_form.cleaned_data['avatar']
            user.profile.birth_date = profile_form.cleaned_data['birth_date']
            user.profile.save()

            messages.success(request, 'Успешная регистрация!')
            return redirect('/login/')
        else:
            messages.error(request, f'Пожалуйста, исправьте ошибки.')
    else:
        user_form = UserForm()
        profile_form = ProfileForm()
    return render(request, 'register.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
