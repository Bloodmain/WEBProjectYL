from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View
from django.views.generic import TemplateView, FormView


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request):
        return render(request, self.template_name, {})


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = '/'
    template_name = 'login.html'

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
