from django.urls import path

from . import views


urlpatterns = [
    path('', views.news_form),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.register),
    path('api/likes/', views.LikeApiView.as_view()),
    path('api/likes/<str:unique_parameter>', views.LikeApiView.as_view()),
    path('api/comments/', views.CommentaryAPI.as_view()),
    path('api/comments/<int:post_id>/<int:user_id>/', views.CommentaryListAPI.as_view()),
    path('api/comments/<str:unique_parameter>/', views.CommentaryAPI.as_view())
]
