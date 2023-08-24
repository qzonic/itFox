from django.shortcuts import get_object_or_404
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from main.models import News


class CreateDestroyModelMixin(mixins.CreateModelMixin,
                              mixins.DestroyModelMixin,
                              GenericViewSet):
    """ Mixin for create ande destroy object. """
    pass


class GetNewsMixin:
    """ Mixin for get news object by id. """

    def get_news(self):
        return get_object_or_404(News, id=self.kwargs['news_id'])


class PerformCreateMixin:
    """ Mixin for set author to object. """

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
