from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (CommentSerializer,
                          ShortNewsSerializer,
                          FullNewsSerializer,)
from .permissions import IsAuthorOrReadOnly
from .mixins import GetNewsMixin, PerformCreateMixin
from main.models import News, Like


class NewsViewSet(PerformCreateMixin, viewsets.ModelViewSet):
    """ ViewSet for retrieve, list, create, update, destroy news. """

    queryset = News.objects.all()
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['create', 'retrieve', 'update']:
            return FullNewsSerializer
        return ShortNewsSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['post'],
        url_path='likes',
        permission_classes=[IsAuthorOrReadOnly]
    )
    def like(self, request, pk):
        news = get_object_or_404(News, id=pk)
        like, created = Like.objects.get_or_create(
            news=news,
            author=request.user
        )
        if created:
            data = {
                'message': 'Лайк добавлен.'
            }
            return Response(data, status.HTTP_201_CREATED)
        data = {
            'error': 'Вы уже поставили лайк этой новости!'
        }
        return Response(data, status.HTTP_400_BAD_REQUEST)

    @like.mapping.delete
    def delete_like(self, request, pk):
        news = get_object_or_404(News, id=pk)
        like = Like.objects.filter(
            author=request.user,
            news=news
        )
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не ставили лайк этой новости!!'},
            status.HTTP_400_BAD_REQUEST
        )


class CommentViewSet(GetNewsMixin, viewsets.ModelViewSet):
    """ ViewSet for retrieve, list, create, update, destroy comment. """

    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        return self.get_news().news_comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, news=self.get_news())
