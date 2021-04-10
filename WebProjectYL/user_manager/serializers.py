from rest_framework import serializers
from .models import Likes, Commentary


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user', 'post', 'unique_parameter']

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentary
        fields = ['user', 'post', 'text', 'unique_parameter']

    def create(self, validated_data):
        return Commentary.objects.create(**validated_data)