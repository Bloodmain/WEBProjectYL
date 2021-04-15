from django.contrib import admin
from .models import Profile, News, Commentary, NewsFile, Repost, Posts, Likes, FriendShip, FriendRequest


class AdminProfile(admin.ModelAdmin):
    list_display = ['user', 'name', 'surname', 'birth_date']
    list_filter = ['name', 'surname', 'birth_date']
    list_display_links = ['user', 'name', 'surname', 'birth_date']
    search_fields = ['user', 'name', 'surname', 'birth_date']

    class Meta:
        model = Profile


class AdminFriendShip(admin.ModelAdmin):
    class Meta:
        model = FriendShip


class AdminFriendRequest(admin.ModelAdmin):
    class Meta:
        model = FriendRequest


class AdminNews(admin.ModelAdmin):
    list_display = ['user', 'likes', 'create_date']
    search_fields = ['user', 'text_content', 'create_date']
    list_filter = ['user', 'likes', 'text_content', 'create_date']

    class Meta:
        model = News


class AdminRepost(admin.ModelAdmin):
    list_display = ['posts', 'user', 'create_date']
    search_fields = ['posts', 'user', 'create_date']
    list_filter = ['posts', 'user', 'create_date']

    class Meta:
        model = Repost


class AdminPosts(admin.ModelAdmin):
    pass


class AdminLikes(admin.ModelAdmin):
    pass


class AdminNewsFiles(admin.ModelAdmin):
    list_display = ['news', 'file']
    search_fields = ['news', 'file']
    list_filter = ['news', 'file']

    class Meta:
        model = NewsFile


class AdminCommentary(admin.ModelAdmin):
    list_display = ['user', 'post']
    search_fields = ['user', 'post', 'text']
    list_filter = ['user', 'post']

    class Meta:
        model = Commentary


# Register your models here.
admin.site.register(Profile, AdminProfile)
admin.site.register(News, AdminNews)
admin.site.register(Commentary, AdminCommentary)
admin.site.register(NewsFile, AdminNewsFiles)
admin.site.register(Repost, AdminRepost)
admin.site.register(Posts, AdminPosts)
admin.site.register(Likes, AdminLikes)
admin.site.register(FriendShip, AdminFriendShip)
admin.site.register(FriendRequest, AdminFriendRequest)