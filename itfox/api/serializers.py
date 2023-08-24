from django.contrib.auth import get_user_model
from rest_framework import serializers

from main.models import Comment, News, Like


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """ User model serializer. """

    class Meta:
        model = User
        fields = (
            'id',
            'username'
        )


class ShortNewsSerializer(serializers.ModelSerializer):
    """ Short news model serializer. """

    author = UserSerializer(read_only=True)

    class Meta:
        model = News
        fields = (
            'id',
            'header',
            'author',
            'published_at',
        )


class FullNewsSerializer(serializers.ModelSerializer):
    """ Full news model serializer."""

    author = UserSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField(read_only=True)
    is_liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = News
        fields = (
            'id',
            'header',
            'published_at',
            'text',
            'author',
            'likes_count',
            'is_liked',
        )
        read_only_fields = (
            'id',
            'published_at',
        )

    def get_likes_count(self, obj):
        return obj.news_likes.count()

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if not user.is_anonymous:
            return Like.objects.filter(author=user, news=obj).exists()
        return False


class CommentSerializer(serializers.ModelSerializer):
    """ Comment model serializer. """

    author = UserSerializer(read_only=True)
    news = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'news',
            'author',
            'published_at',
        )
