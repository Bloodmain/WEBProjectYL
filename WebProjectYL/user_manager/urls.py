from django.urls import path

from . import views


urlpatterns = [
    path('', views.news_form),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.register),
    path('homepage/<int:user_id>', views.homepage),
    path('homepage/unknown', views.unknown_homepage)
]
