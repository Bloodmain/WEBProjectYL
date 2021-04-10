from rest_framework import serializers
from .models import Likes, Commentary, Profile


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
        fields = ['user', 'post', 'text', 'unique_parameter']

    def create(self, validated_data):
        return Commentary.objects.create(**validated_data)