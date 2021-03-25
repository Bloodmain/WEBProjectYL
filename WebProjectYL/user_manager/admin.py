from django.contrib import admin
from .models import Profile, News, Commentary


class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'name', 'surname', 'birth_date']
    list_filter = ['name', 'surname', 'birth_date']
    list_display_links = ['user', 'name', 'surname', 'birth_date']
    search_fields = ['user', 'name', 'surname', 'birth_date']

    class Meta:
        model = Profile


class AdminNews(admin.ModelAdmin):
    list_display = ['user', 'likes']
    search_fields = ['user', 'text_content']
    list_filter = ['user', 'likes', 'text_content']

    class Meta:
        model = News


class AdminCommentary(admin.ModelAdmin):
    list_display = ['user', 'news']
    search_fields = ['user', 'news', 'text']
    list_filter = ['user', 'news']

    class Meta:
        model = Commentary


# Register your models here.
admin.site.register(Profile, AdminProfile)
admin.site.register(News, AdminNews)
admin.site.register(Commentary, AdminCommentary)