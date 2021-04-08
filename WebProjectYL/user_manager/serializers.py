from rest_framework import serializers
from .models import Likes


class LikesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = ['user', 'post', 'unique_parameter']

    def create(self, validated_data):
        return Likes.objects.create(**validated_data)