from django.urls import path

from . import views


urlpatterns = [
    path('', views.news_form),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.Logout.as_view()),
    path('register/', views.register),
    path('homepage/<int:user_id>', views.homepage),
    path('homepage/unknown', views.unknown_homepage),
    path('api/user', views.UserApi.as_view()),
    path('api/likes', views.LikeApiView.as_view()),
    path('api/likes/<str:unique_parameter>', views.LikeApiView.as_view()),
    path('api/comments', views.CommentaryAPI.as_view()),
    path('api/comments/<int:post_id>/<int:user_id>', views.CommentaryListAPI.as_view()),
    path('api/comments/<int:pk>', views.CommentaryAPI.as_view()),
    path('api/news/<int:news_id>', views.NewsAPI.as_view())
]
