from django.contrib import messages
from django.contrib.auth import login, logout
from .forms import UserLoginForm, UserForm, ProfileForm, NewsForm
from django.shortcuts import render, redirect
from .models import NewsFile, News, Likes, Commentary
from .serializers import LikesSerializer, CommentsSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

# Create your views here.
from django.views import View
from django.views.generic import FormView
import os


class LikeApiView(APIView):
    def get(self, request, unique_parameter):
        like = Likes.objects.filter(unique_parameter=unique_parameter).first()
        if not like:
            return Response({"Error": "The object does not exist"})
        ser = LikesSerializer(like)
        return Response({"Like": ser.data})

    def post(self, request):
        data = request.data
        data['unique_parameter'] = f"{data['user']}_{data['post']}"
        like = Likes.objects.filter(unique_parameter=data['unique_parameter'])
        if like.count() != 0:
            return Response({"Error": "Object already exists"})
        serializer = LikesSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, unique_parameter):
        like = Likes.objects.filter(unique_parameter=unique_parameter).first()
        if not like:
            return Response({"Error": "The object does not exist"})
        like.delete()
        return Response({"Success": "OK"})


class CommentaryAPI(APIView):
    def get(self, request, unique_parameter):
        comment = Commentary.objects.filter(unique_parameter=unique_parameter).first()
        if not comment:
            return Response({"Error": "The object does not exist"})
        ser_comment = CommentsSerializer(comment)
        return Response({"Comment": ser_comment.data})

    def post(self, request):
        data = request.data
        if any([i not in data for i in ['user', 'post', 'text']]):
            return Response({"Error": "Not all parameters are listed"})
        comments = Commentary.objects.filter(user=data['user'], post=data['post'])
        mx_number = 0
        for comment in comments:
            mx_number = max(mx_number, int(comment.unique_parameter.split('_')[2]))
        mx_number += 1
        data['unique_parameter'] = f"{data['post']}_{data['user']}_{mx_number}"
        ser = CommentsSerializer(data=data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({"Success": "OK", "Number comment": data['unique_parameter']})
        return Response({"Error": "Bad request"})

    def delete(self, request, unique_parameter):
        comment = Commentary.objects.filter(unique_parameter=unique_parameter).first()
        if not comment:
            return Response({"Error": "The object does not exist"})
        comment.delete()
        return Response({"Success": "OK"})


class CommentaryListAPI(APIView):
    def get(self, request, user_id, post_id):
        comments = Commentary.objects.filter(user=user_id, post=post_id)
        ser = CommentsSerializer(comments, many=True)
        return Response({"Comments": ser.data})


def news_form(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = News.objects.create(user=request.user,
                                       text_content=form.cleaned_data['text_content'])
            for file in request.FILES.getlist('attachments'):
                NewsFile.objects.create(file=file, news=news)
            news.save()
            return redirect('/')
    else:
        form = NewsForm()
    if request.user.is_authenticated:
        all_news = request.user.profile.get_news_interesting_for_user()
        images = {}
        width = {}
        for news in all_news:
            for file in news.files.all():
                url = file.file.url
                if url.rsplit('.', 1)[-1] in {'png', 'jpg', 'jpeg'}:
                    images[news] = images.get(news, set()) | {file}
            if news in images:
                width[news] = 100 // min(len(images[news]), 3)
        return render(request, 'main.html',
                      {'form': form,
                       'all_news': all_news,
                       'images': images,
                       'widths': width})
    else:
        return render(request, 'main.html',
                      {'form': form, 'all_news': [], 'images': {}, 'widths': {}})


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
