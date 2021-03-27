from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


def avatars_directory(instance, filename):
    return f"users/{instance.user.id}/avatar.jpg"


def news_files_directory(instance, filename):
    return f"news/{instance.news.id}/files/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, verbose_name="Имя", null=True, blank=False)
    surname = models.CharField(max_length=75, verbose_name="Фамилия", null=True, blank=False)
    bio = models.TextField(max_length=500, verbose_name="Описание", default="", null=True,
                           blank=False)
    avatar = models.ImageField(verbose_name="Фото", null=True, upload_to=avatars_directory)
    status = models.CharField(max_length=75, default="", verbose_name="Статус", null=True,
                              blank=False)
    birth_date = models.DateField(verbose_name='Дата рождения', null=True, blank=False)

    def get_news_interesting_for_user(self):
        return self.user.news.all

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


class News(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news')
    text_content = models.TextField(max_length=1000, verbose_name='Контент', blank=False)
    likes = models.IntegerField(default=0, verbose_name='Лайки')

    def __str__(self):
        return self.text_content[:20] + "..."

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class NewsFile(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(null=True, blank=True, upload_to=news_files_directory)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"


class Commentary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comment')
    text = models.TextField(max_length=100, null=False, blank=False, default="")

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Коммментарии"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
