from rest_framework import serializers
from .models import Likes, Commentary, Profile, Repost, FriendShip, FriendRequest, SubscriberShip


class RepostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repost
        fields = ['pk', 'posts', 'user', 'create_date']

    def create(self, validated_data):
        return Repost.objects.create(**validated_data)


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user', 'post', 'unique_parameter']

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'name', 'surname', 'bio', 'status', 'birth_date']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ['user', 'post', 'text']

    def create(self, validated_data):
        return Commentary.objects.create(**validated_data)


class FriendShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendShip
        fields = ['creator', 'friend', 'create_date']


class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = FriendRequest
        fields = ['requester', 'friend', 'create_date']


class SubscriberShipSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriberShip
        fields = ['subscriber', 'author', 'create_date']
