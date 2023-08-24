from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from .views import (
    CommentViewSet,
    NewsViewSet,
)


router = DefaultRouter()
router.register(
    'news',
    NewsViewSet,
    basename='news',
)
router.register(
    r'news/(?P<news_id>\d+)/comments',
    CommentViewSet,
    basename='comments',
)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
