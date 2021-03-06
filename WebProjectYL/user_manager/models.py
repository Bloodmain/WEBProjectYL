from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime
import random


# Create your models here.


def community_avatar_directory(instance, filename):
    return f"community/{instance.id}/avatar.jpg"


def community_post_directory(instance, filename):
    return f"community_post/{instance.c_post.id}/files/{filename}"


def avatars_directory(instance, filename):
    return f"users/{instance.user.id}/avatar.jpg"


def news_files_directory(instance, filename):
    return f"news/{instance.news.id}/files/{filename}"


class Profile(models.Model):
    """
    Модель Profile является оберткой для модели User, встроенной в Django по умолчанию
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, verbose_name="Имя", null=True, blank=False)
    surname = models.CharField(max_length=75, verbose_name="Фамилия", null=True, blank=False)
    bio = models.TextField(max_length=500, verbose_name="Описание", default="", null=True,
                           blank=False)
    avatar = models.ImageField(verbose_name="Фото", null=True, upload_to=avatars_directory)
    status = models.CharField(max_length=75, default="", verbose_name="Статус", null=True,
                              blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=False)
    lname = models.CharField(max_length=50, verbose_name="Имя в нижнем регистре", null=True,
                             blank=False)
    lsurname = models.CharField(max_length=75, verbose_name="Фамилия в нижнем регистре", null=True,
                                blank=False)

    def get_our_news(self):
        """
        Возвращает список наших новостей
        """
        return self.user.news.all()

    def get_our_reposts(self):
        """
        Возвращает список наших репостов
        """
        return self.user.repost.all()

    def get_news_interesting_for_user(self):
        """
        Формирует интересные новости для пользователя
        """
        news = []
        for friend in self.get_friends():
            for post in friend.profile.get_our_reposts():
                news.append(post)
            for post in friend.profile.get_our_news():
                news.append(post)
        for friend in self.get_our_friends_request():
            for post in friend.profile.get_our_reposts():
                news.append(post)
            for post in friend.profile.get_our_news():
                news.append(post)
        for author in self.get_authors():
            for post in author.profile.get_our_reposts():
                news.append(post)
            for post in author.profile.get_our_news():
                news.append(post)
        for post in self.get_our_news():
            news.append(post)
        for com in self.get_communities():
            for post in com.news.all():
                news.append(post)
        return sorted(news, key=lambda x: x.create_date, reverse=True)

    def get_friends_request(self):
        """Возвращает все кто отправил нам запрос в друзья"""
        return [request.requester for request in self.user.FriendRequests.all()]

    def get_our_friends_request(self):
        """Возвращает всех людей которым мы отправили запрос на дружбу"""
        return [request.friend for request in self.user.our_requests.all()]

    def get_friends(self):
        """Возвращает всех наших друзей"""
        return [friend_ship.friend for friend_ship in self.user.creator.all()] + \
               [friend_ship.creator for friend_ship in self.user.friends.all()]

    def get_subscribers(self):
        """Возвращает всех наших подписчиков"""
        return [subscriber_ship.subscriber for subscriber_ship in self.user.author.all()]

    def get_authors(self):
        """Возвращает всех на кого мы подписаны"""
        return [subscriber_ship.author for subscriber_ship in self.user.subscriber.all()]

    def get_communities(self):
        """Возвращает все сообщества, в которых мы состоим"""
        return list(
            set(self.user.communities_creator.all()) | set(self.user.communities_admin.all()) | set(
                self.user.communities.all()))

    def is_friends(self, other):
        """
        other -> User
        Возращает взаимоотношение между пользователями
        0 - не друзья
        1 - друзья
        2 - мы сделали запрос
        3 - он сделал запрос
        4 - он наш подписчик
        5 - мы его подписчик
        6 - это мы
        """
        if other == self.user:
            return 6
        if other in self.get_friends():
            return 1
        if other in self.get_our_friends_request():
            return 2
        if other in self.get_friends_request():
            return 3
        if other in self.get_subscribers():
            return 4
        if other in self.get_authors():
            return 5
        return 0

    def __str__(self):
        return self.user.username

    def get_full_name(self):
        return self.surname + " " + self.name

    def get_short_name(self):
        return self.name

    class Meta:
        ordering = ['name', 'surname', 'birth_date']
        verbose_name = "Профлиль пользователя"
        verbose_name_plural = "Профили пользователей"


class Community(models.Model):
    """
    Модель для сообществ. Содержит название, описание, создателя, аватарку, админов и участников
    """
    creator = models.ForeignKey(User, related_name="communities_creator", on_delete=models.CASCADE)
    title = models.CharField(max_length=75, verbose_name="Название сообщества", null=True,
                             blank=False)
    describe = models.TextField(max_length=1000, verbose_name="Описание сообщества", null=True,
                                blank=False)
    avatar = models.FileField(null=True, blank=True, upload_to=community_avatar_directory)
    admins = models.ManyToManyField(User, related_name="communities_admin", verbose_name="Админы",
                                    null=True, blank=True)
    members = models.ManyToManyField(User, related_name="communities", verbose_name="Подписчики",
                                     null=True, blank=True)

    def get_user_status(self, user):
        if user == self.creator:
            return 1
        elif user in self.admins.all():
            return 2
        elif user in self.members.all():
            return 3
        else:
            return 0

    class Meta:
        verbose_name = 'Сообщество'
        verbose_name_plural = 'Сообщества'


class Chat(models.Model):
    """
    Модель чата. Содержит тип и участников чата.
    """
    CHAT = 'C'
    DIALOG = 'D'
    TYPES = (
        (CHAT, 'Chat'),
        (DIALOG, 'Dialog')
    )
    type = models.CharField(verbose_name='Тип', max_length=1, choices=TYPES, default=DIALOG)
    members = models.ManyToManyField(User, verbose_name='Участник', related_name='chats')

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    """
    Модель сообщения. Содержит автор, чат, текст а так же дату отправки сообщения
    """
    text = models.CharField(max_length=1000, verbose_name='Текст сообщения', default="")
    author = models.ForeignKey(User, verbose_name="Автор", related_name="message",
                               on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, verbose_name="Чат", related_name="message",
                             on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="Дата создания", default=datetime.datetime.now)

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.text


class FriendRequest(models.Model):
    """
    Модель запроса в друзьях. В описание поле написано кто что делает
    """
    requester = models.ForeignKey(User, on_delete=models.CASCADE,
                                  verbose_name="тот кто отправляет запрос",
                                  related_name="our_requests")
    friend = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name="кому отправлен запрос", related_name="FriendRequests")
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = "Запрос в друзья"
        verbose_name_plural = "Запросы в друзья"


class FriendShip(models.Model):
    """
    Модель дружбы. В описание поле написано кто что делает
    """
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Первый друг",
                                related_name="creator")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Второй друг",
                               related_name="friends")
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = "Дружба"
        verbose_name_plural = "Дружбы"


class SubscriberShip(models.Model):
    """
    Модель подписки. В описание поле написано кто что делает
    """
    subscriber = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Подписчик",
                                   related_name='subscriber')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="На кого подписан",
                               related_name='author')
    create_date = models.DateTimeField(verbose_name="дата создания", default=datetime.datetime.now)

    class Meta:
        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"


class News(models.Model):
    """
    Модель новости содержит автора, текс, количество лайков и дату создания
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    text_content = models.TextField(max_length=1000, verbose_name='Контент', blank=False)
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsFile(models.Model):
    """
    Файлы прикрепленные к новости
    """
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(null=True, blank=True, upload_to=news_files_directory)

    class Meta:
        verbose_name = "Файл новости"
        verbose_name_plural = "Файлы новостей"


class Repost(models.Model):
    """
    Репост содержит. Пост репост которого сделан и пользователя сделавшего репост.
    """
    posts = models.ForeignKey("Posts", on_delete=models.CASCADE, related_name='repost')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='repost')
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = 'Репост'
        verbose_name_plural = 'Репосты'


class CommunityPost(models.Model):
    """
    Новости сообщества. См модель News
    """
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name="news")
    text_content = models.TextField(max_length=1000, verbose_name='Контент', blank=False)
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    class Meta:
        verbose_name = "Новость сообщества"
        verbose_name_plural = "Новости сообществ"


class CommunityPostFiles(models.Model):
    """
    Файлы прикрепленные к новости сообщества
    """
    c_post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(null=True, blank=True, upload_to=community_post_directory)

    class Meta:
        verbose_name = "Файл новости"
        verbose_name_plural = "Файлы новостей"


class Posts(models.Model):
    """
    Модель обобщающая news, reposts, community_news
    """
    news = models.OneToOneField(News, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='post')
    reposts = models.OneToOneField(Repost, on_delete=models.CASCADE, null=True, blank=True,
                                   related_name='post')
    community_news = models.OneToOneField(CommunityPost, on_delete=models.CASCADE, null=True,
                                          blank=True,
                                          related_name="post")

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    @property
    def total_likes(self):
        return self.likes.count()


class Likes(models.Model):
    """
    Модель лайка. Содержит пользователя и пост.
    Уникальный параметр нужен чтобы отличать пользователь не мог поставить лайк к одной и той же записи
    """
    user = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, related_name='likes', on_delete=models.CASCADE)
    unique_parameter = models.CharField(max_length=50, verbose_name='Уникальный параметр',
                                        blank=True, null=False,
                                        unique=True)

    class Meta:
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"


class Commentary(models.Model):
    """
    Модель комментария. Содержит пользователя, пост и текст, а так же дату создания.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField(max_length=1000, null=False, blank=False, default="")
    create_date = models.DateTimeField(verbose_name='дата создания', default=datetime.datetime.now)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Коммментарии"


@receiver(post_save, sender=CommunityPost)
def create_post_on_сnews(sender, instance, created, **kwargs):
    if created:
        Posts.objects.create(community_news=instance)


@receiver(post_save, sender=CommunityPost)
def save_post_on_сnews(sender, instance, **kwargs):
    instance.post.save()


@receiver(post_save, sender=News)
def create_post_on_news(sender, instance, created, **kwargs):
    if created:
        Posts.objects.create(news=instance)


@receiver(post_save, sender=News)
def save_post_on_news(sender, instance, **kwargs):
    instance.post.save()


@receiver(post_save, sender=Repost)
def create_post_on_repost(sender, instance, created, **kwargs):
    if created:
        Posts.objects.create(reposts=instance)


@receiver(post_save, sender=Repost)
def save_post_on_repost(sender, instance, **kwargs):
    instance.posts.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
