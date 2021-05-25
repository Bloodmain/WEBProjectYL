from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import UserLoginForm, UserForm, ProfileForm, NewsForm
from django.shortcuts import render, redirect
from .models import NewsFile, News, Likes, Commentary, Repost, Posts, Profile, FriendShip, \
    FriendRequest, SubscriberShip, Message, Chat, Community
from .serializers import LikesSerializer, UserSerializer, CommentsSerializer, RepostSerializer, \
    FriendShipSerializer, ChatSerializer, CommunitySerializer, CommunityAddSerializer
from .serializers import FriendRequestSerializer, SubscriberShipSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import datetime
import requests

# Create your views here.
from django.views import View
from django.views.generic import FormView
import os


def get_news_data(all_news):
    images = []
    width = []
    comments = []

    for i, (news, tp) in enumerate(all_news):
        if tp == 0:
            reposted = news
            news = news.posts
            while news.news is None:
                news = news.reposts.posts
            news = news.news
            all_news[i][0].text_content = news.text_content
            all_news[i][0].files = news.files
        to_add = []
        for file in news.files.all():
            url = file.file.url
            if url.rsplit('.', 1)[-1] in {'png', 'jpg', 'jpeg'}:
                to_add.append(file)
        images.append(to_add)
        if tp == 1:
            comments.append(news.post.comment.all())
        else:
            comments.append(reposted.post.comment.all())

        if to_add:
            width.append(100 // min(len(to_add), 3))
        else:
            width.append(-1)

    return images, width, comments


class UserApi(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthenticated user'})
        user = request.user.profile
        serializer = UserSerializer(user)
        return Response({'user': serializer.data})


class FindPost(APIView):
    def get(self, request, repost_id):
        repost = Repost.objects.filter(pk=repost_id).first()
        if not repost:
            return Response({"Error": "The object does not exist"})
        post = repost.posts
        ans = post.pk
        while post.news is None:
            post = post.reposts.posts
            ans = post.pk
        return Response({"Post_id": str(ans)})


class SearchCommunityApi(APIView):
    def get(self, request, community_title):
        communties = Community.objects.filter(title__contains=community_title).all()
        ser = CommentsSerializer(communties, many=True)
        return Response({"Communities": ser.data})


class UserCommunityStatus(APIView):
    def get(self, request, community_pk, user_pk):
        community = Community.objects.filter(pk=community_pk).first()
        if not community:
            return Response({"Error": "Community does not exist"})
        user = User.objects.filter(pk=user_pk).first()
        if not user:
            return Response({"Error": "User does not exist"})
        answer = {
            0: Response({"Status": 0,
                         "Message": "Has no connections"}),
            1: Response({"Status": 1,
                         "Message": "Сreator"}),
            2: Response({"Status": 2,
                         "Message": "Admin"}),
            3: Response({"Status": 3,
                         "Message": "Member"})
        }
        status = community.get_user_status(user)
        return answer[status]

    def post(self, request):
        data = request.data.copy()
        user_pk = data['user_pk']
        community_pk = data['community_pk']
        status = int(data['status'])
        community = Community.objects.filter(pk=community_pk).first()
        if not community:
            return Response({"Error": "Community does not exist"})
        user = User.objects.filter(pk=user_pk).first()
        if not user:
            return Response({"Error": "User does not exist"})
        if status == 2:
            community.admins.add(user)
        elif status == 3:
            print(status)
            community.members.add(user)
        else:
            return Response({"Error": "Status error"})
        return Response({"Success": "OK"})

    def delete(self, request, community_pk, user_pk, status):
        community = Community.objects.filter(pk=community_pk).first()
        if not community:
            return Response({"Error": "Community does not exist"})
        user = User.objects.filter(pk=user_pk).first()
        if not user:
            return Response({"Error": "User does not exist"})
        if status == 2 and community.get_user_status(user) == 2:
            community.admins.remove(user)
            return Response({"Success": "OK"})
        elif status == 3 and community.get_user_status(user) == 3:
            community.admins.remove(user)
            return Response({"Success": "OK"})
        else:
            return Response({"Error": "Status error"})


class CommunityApi(APIView):
    def get(self, request, pk):
        community = Community.objects.filter(pk=pk).first()
        if not community:
            return Response({"Error": "The object does not exist"})
        ser = CommunitySerializer(community)
        return Response({"Community": ser.data})

    def post(self, request):
        data = request.data.copy()
        ser = CommunityAddSerializer(data=data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, pk):
        community = Community.objects.filter(pk=pk).first()
        if not community:
            return Response({"Error": "The object does not exist"})
        community.delete()
        return Response({"Success": "OK"})


class LikeApiView(APIView):
    def get(self, request, unique_parameter):
        like = Likes.objects.filter(unique_parameter=unique_parameter).first()
        if not like:
            return Response({"Error": "The object does not exist"})
        ser = LikesSerializer(like)
        return Response({"Like": ser.data})

    def post(self, request):
        data = request.data.copy()
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
    def get(self, request, pk):
        comment = Commentary.objects.filter(pk=pk).first()
        if not comment:
            return Response({"Error": "The object does not exist"})
        ser_comment = CommentsSerializer(comment)
        return Response({"Comment": ser_comment.data})

    def post(self, request):
        data = request.data.copy()
        if any([i not in data for i in ['user', 'post', 'text']]):
            return Response({"Error": "Not all parameters were used"})
        ser = CommentsSerializer(data=data)
        if ser.is_valid(raise_exception=True):
            ser.save()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, pk):
        comment = Commentary.objects.filter(pk=pk).first()
        if not comment:
            return Response({"Error": "The object does not exist"})
        comment.delete()
        return Response({"Success": "OK"})


class RepostListAPI(APIView):
    def get(self, request):
        reposts = Repost.objects.all()
        serializer = RepostSerializer(reposts, many=True)
        return Response({"Reposts": serializer.data})

    def post(self, request):
        data = request.data.copy()
        if any([i not in data for i in ['user', 'posts']]):
            return Response({"Error": "Not all parameters were used"})
        data['create_date'] = datetime.datetime.now()
        serializer = RepostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})


class RepostAPI(APIView):
    def get(self, request, pk):
        repost = Repost.objects.filter(pk=pk).first()
        if not repost:
            return Response({"Error": "The object does not exist"})
        serializer = RepostSerializer(repost)
        return Response({"Repost": serializer.data})

    def delete(self, request, pk):
        repost = Repost.objects.filter(pk=pk).first()
        if not repost:
            return Response({"Error": "The object does not exist"})
        repost.delete()
        return Response({"Succcess": "OK"})


class CommentaryListAPI(APIView):
    def get(self, request, user_id, post_id):
        comments = Commentary.objects.filter(user=user_id, post=post_id)
        ser = CommentsSerializer(comments, many=True)
        return Response({"Comments": ser.data})


class NewsAPI(APIView):
    def delete(self, request, news_id):
        news = News.objects.filter(id=news_id).first()
        if not news:
            return Response({"Error": "The object does not exist"})
        news.delete()
        return Response({"Success": "OK"})


def show_post(request, post_id):
    post = Posts.objects.filter(pk=post_id).first()
    if post.news is None:
        post = [(post.reposts, 0)]
    else:
        post = [(post.news, 1)]
    images, width, comments = get_news_data(post)
    return render(request, 'one_post.html',
                  {'news': post[0][0],
                   'images': images[0],
                   'width': width[0],
                   'comments': comments[0],
                   'tp': isinstance(post[0][0], News),
                   'title': 'Новость'})


def repost_origin(request, repost_id):
    post_id = Repost.objects.filter(pk=repost_id).first().posts.id
    return redirect(f'/show_post/{post_id}')


class SearchUserAPI(APIView):
    def get(self, request, request_api):
        name = request_api.split('~')
        if len(name) > 2:
            return Response({"Error": "Bad request"})
        if len(name) == 1:
            name = name[0].replace('_', ' ')
            users_1 = Profile.objects.filter(name__icontains=name)
            users_2 = Profile.objects.filter(surname__icontains=name)
            users = users_1 | users_2
            serializer = UserSerializer(users, many=True)
            return Response({"Users": serializer.data})
        name, surname = name[0].replace('_', ' '), name[1].replace('_', ' ')
        users_1 = Profile.objects.filter(name__icontains=name, surname__icontains=surname)
        users_2 = Profile.objects.filter(surname__icontains=name, name__icontains=surname)
        users = users_1 | users_2
        serializer = UserSerializer(users, many=True)
        return Response({"Users": serializer.data})


class UsersRelationship(APIView):
    def get(self, request, user1_id, user2_id):
        user1 = User.objects.filter(pk=user1_id).first()
        user2 = User.objects.filter(pk=user2_id).first()
        if not user1 or not user2:
            return Response({"Error": "User does not exist"})
        status = user1.profile.is_friends(user2)
        answer = {0: Response({"Status": 0, "Message": "Not friends"}),
                  1: Response({"Status": 1, "Message": "Friends"}),
                  2: Response({"Status": 2, "Message": "User1 made a request to User2"}),
                  3: Response({"Status": 3, "Message": "User2 made a request to User1"}),
                  4: Response({"Status": 4, "Message": "User2 is subscribed to User1"}),
                  5: Response({"Status": 5, "Message": "User1 is subscribed to User2"}),
                  6: Response({"Status": 6, "Message": "The objects are the same"})}
        return answer[status]


class FriendsAPI(APIView):
    def get(self, request, user_id):
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return Response({"Error": "User does not exist"})
        friends_ships = FriendShip.objects.filter(Q(creator=user) | Q(friend=user))
        serializer = FriendShipSerializer(friends_ships, many=True)
        return Response({"Friends": serializer.data})

    def post(self, request):
        data = request.data.copy()
        if any([i not in data for i in ['creator', 'friend']]):
            return Response({"Error": "Not all parameters were used"})
        user1 = User.objects.filter(pk=data['creator']).first()
        user2 = User.objects.filter(pk=data['friend']).first()
        print(user2, user1)
        if not user1 or not user2:
            return Response({"Error": "User does not exist"})
        status = user1.profile.is_friends(user2)
        if status != 2 and status != 3 and status != 5:
            return Response({"Error": "UsersRelationship error",
                             "UsersRelationship": status})
        if status == 2:
            friend_req = FriendRequest.objects.filter(requester=user1, friend=user2).first()
        elif status == 3:
            friend_req = FriendRequest.objects.filter(requester=user2, friend=user1).first()
        elif status == 5:
            friend_req = SubscriberShip.objects.filter(author=user2, subscriber=user1).first()
        serializer = FriendShipSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            friend_req.delete()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, user1_id, user2_id):
        friend_ship = FriendShip.objects.filter(Q(creator=user1_id, friend=user2_id) |
                                                Q(creator=user2_id, friend=user1_id)).first()
        if not friend_ship:
            return Response({"Error": "The object does not exist"})
        friend_ship.delete()
        return Response({"Success": "OK"})


class FriendsRequestAPI(APIView):
    def get(self, request, user1_id, user2_id):
        """
        status:
        0 - вернуть наши запросы и запросы к нам
        1 - вернуть наши запросы
        2 - вернуть запросы к нам
        """
        user_id, status = user1_id, user2_id
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return Response({"Error": "User does not exist"})
        if status < 0 or status > 2:
            return Response({"Error": "Invalid 'status' value"})
        if status == 0:
            req = FriendRequest.objects.filter(Q(requester=user) | Q(friend=user))
        elif status == 1:
            req = FriendRequest.objects.filter(requester=user)
        else:
            req = FriendRequest.objects.filter(friend=user)
        serializer = FriendRequestSerializer(req, many=True)
        return Response({"FriendsRequests": serializer.data})

    def post(self, request):
        data = request.data.copy()
        if any([i not in data for i in ['requester', 'friend']]):
            return Response({"Error": "Not all parameters were used"})
        user1 = User.objects.filter(pk=data['requester']).first()
        user2 = User.objects.filter(pk=data['friend']).first()
        if not user1 or not user2:
            return Response({"Error": "User does not exist"})
        status = user1.profile.is_friends(user2)
        if status != 0:
            return Response({"Error": "UsersRelationship error",
                             "UsersRelationship": status})
        serializer = FriendRequestSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, user1_id, user2_id):
        friends_req = FriendRequest.objects.filter(Q(requester=user1_id, friend=user2_id) |
                                                   Q(requester=user2_id, friend=user1_id))
        if not friends_req:
            return Response({"Error": "The object does not exist"})
        friends_req.delete()
        return Response({"Success": "OK"})


class StatusAPI(APIView):
    def put(self, request):
        if any([i not in request.data for i in ['uid', 'new_value']]):
            return Response({"Error": "Not all parameters were used"})
        uid, new_value = request.data['uid'], request.data['new_value']
        user = User.objects.filter(id=uid).first()
        if not user:
            return Response({'Error': 'User does not exist'})
        if user.profile.status != new_value:
            user.profile.status = new_value
        user.profile.save()
        return Response({'Success': 'OK'})


class SubscriberAPI(APIView):
    def get(self, request, user1_id, user2_id):
        """
        status:
        0 - вернуть наших подписчиков и на кого мы подписаны
        1 - вернуть наших подписчиков
        2 - вернуть на кого мы подписаны
        """
        user_id, status = user1_id, user2_id
        user = User.objects.filter(pk=user_id).first()
        if not user:
            return Response({"Error": "User does not exist"})
        if status < 0 or status > 2:
            return Response({"Error": "Invalid 'status' value"})
        if status == 0:
            req = SubscriberShip.objects.filter(Q(subscriber=user) | Q(author=user))
        elif status == 1:
            req = SubscriberShip.objects.filter(author=user)
        else:
            req = SubscriberShip.objects.filter(subscriber=user)
        serializer = SubscriberShipSerializer(req, many=True)
        return Response({"SubscriberShip": serializer.data})

    def post(self, request):
        data = request.data.copy()
        if any([i not in data for i in ['subscriber', 'author']]):
            return Response({"Error": "Not all parameters were used"})
        user1 = User.objects.filter(pk=data['author']).first()
        user2 = User.objects.filter(pk=data['subscriber']).first()
        if not user1 or not user2:
            return Response({"Error": "User does not exist"})
        status = user1.profile.is_friends(user2)
        if status != 3:
            return Response({"Error": "UsersRelationship error",
                             "UsersRelationship": status})
        req = FriendRequest.objects.filter(requester=data['subscriber'],
                                           friend=data['author']).first()
        serializer = SubscriberShipSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            req.delete()
            return Response({"Success": "OK"})
        return Response({"Error": "Bad request"})

    def delete(self, request, user1_id, user2_id):
        req = SubscriberShip.objects.filter(Q(subscriber=user2_id, author=user1_id) |
                                            Q(subscriber=user1_id, author=user2_id)).first()
        if not req:
            return Response({"Error": "The object does not exist"})
        req.delete()
        return Response({"Success": "OK"})


class ChatsAPI(APIView):
    def get(self, request, uid1, uid2):
        for chat in Chat.objects.all():
            if uid1 in map(lambda x: x.id, chat.members.all()) and uid2 in map(lambda x: x.id,
                                                                               chat.members.all()):
                ser = ChatSerializer(chat)
                return Response({'Chat': ser.data})
        return Response({'Error': 'The object does not exist'})

    def post(self, request, uid1, uid2):
        if 'Error' in self.get(request, uid1, uid2).data:
            ser = ChatSerializer(data={'members': [uid1, uid2]})
            if ser.is_valid(raise_exception=True):
                ser.save()
                chat = self.get(request, uid1, uid2).data['Chat']['id']
                return Response({'Success': 'OK', 'Chat_id': chat})
            return Response({'Error': 'Bad request'})
        return Response({'Error': 'Object already exists'})


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
        all_news = [(news, isinstance(news, News))
                    for news in request.user.profile.get_news_interesting_for_user()]
    else:
        all_news = [(x, 1)
                    for x in sorted(News.objects.all(), key=lambda x: x.create_date, reverse=True)]

    images, width, comments = get_news_data(all_news)

    return render(request, 'main.html',
                  {'form': form,
                   'all_news': all_news,
                   'images': images,
                   'widths': width,
                   'comments': comments,
                   'title': 'Новости'})


def show_friends(request, user_id):
    user = User.objects.filter(pk=user_id).first()
    friends = list(FriendShip.objects.filter(Q(creator=user) | Q(friend=user)).all())
    subscribers = list(SubscriberShip.objects.filter(author=user).all())
    subscribes = list(SubscriberShip.objects.filter(subscriber=user).all())
    reqs_to_you = list(FriendRequest.objects.filter(friend=user).all())
    your_reqs = list(FriendRequest.objects.filter(requester=user).all())
    return render(request, 'friends.html',
                  {'title': 'Друзья',
                   'friends': friends,
                   'subscribers': subscribers,
                   'subscribes': subscribes,
                   'reqs_to_you': reqs_to_you,
                   'your_reqs': your_reqs,
                   'page_owner': user})


def find_user(request):
    r = request.GET.get('request', '')
    req = r.lower().split(maxsplit=1)
    users = []
    if len(req) == 1:
        name = req[0].replace('_', ' ')
        users_1 = Profile.objects.filter(lname__icontains=name)
        users_2 = Profile.objects.filter(lsurname__icontains=name)
        users = (users_1 | users_2).all()
    elif len(req) == 2:
        name, surname = req[0].replace('_', ' '), req[1].replace('_', ' ')
        users_1 = Profile.objects.filter(lname__icontains=name, lsurname__icontains=surname)
        users_2 = Profile.objects.filter(lsurname__icontains=name, lname__icontains=surname)
        users = (users_1 | users_2).all()

    return render(request, 'find_user.html',
                  {'title': 'Найти',
                   'users': users,
                   'req': r})


def chats(request):
    all_chats = request.user.chats.all()
    return render(request, 'messages.html',
                  {'title': 'Сообщения',
                   'chats': all_chats})


def show_chat(request, chat_id):
    chat = Chat.objects.filter(pk=chat_id).first()
    all_chats = request.user.chats.all()
    return render(request, 'show_chat.html',
                  {'title': 'Сообщения',
                   'chats': all_chats,
                   'selected_chat': chat_id,
                   'chat_to_show': chat})


def show_groups(request, group_id):
    return render(request, 'groups.html',
                  {'title': 'Сообщества'})


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
            user.profile.lname = user_form.cleaned_data['first_name'].lower()
            user.profile.lsurname = user_form.cleaned_data['last_name'].lower()
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
        'profile_form': profile_form,
        'title': 'Регистрация'
    })


def access_denied(request):
    return render(request, 'access_denied.html', {'title': 'Доступ запрещен'})


def homepage(request, user_id):
    user = User.objects.get(id=user_id)
    if request.user.is_authenticated:
        is_friends = request.user.profile.is_friends(user)
    else:
        is_friends = 6
    all_news = [(x, isinstance(x, News))
                for x in sorted(list(user.news.all()) + list(user.repost.all()),
                                key=lambda x: x.create_date, reverse=True)]
    images, width, comments = get_news_data(all_news)
    return render(request, 'homepage.html', {
        'page_owner': user,
        'is_friends': is_friends,
        'images': images,
        'widths': width,
        'all_news': all_news,
        'comments': comments,
        'title': 'Страница пользователя'})
