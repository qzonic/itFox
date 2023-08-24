from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import News, Like


User = get_user_model()


class TestLike(APITestCase):
    """ Test like logic. """

    @classmethod
    def setUpClass(cls):
        super(TestLike, cls).setUpClass()
        cls.first_user = User.objects.create_user(
            username='first_test_user'
        )
        cls.second_user = User.objects.create_user(
            username='second_test_user'
        )
        cls.first_news = News.objects.create(
            header='Test header for first news',
            text='Test text',
            author=cls.first_user,
        )
        cls.second_news = News.objects.create(
            header='Test header for second news',
            text='Test text',
            author=cls.second_user,
        )
        cls.first_like_for_first_news = Like.objects.create(
            author=cls.first_user,
            news=cls.first_news,
        )
        cls.first_like_for_second_news = Like.objects.create(
            author=cls.second_user,
            news=cls.second_news,
        )

    def setUp(self) -> None:
        self.guest_client = APIClient()

        self.first_authorized_client = APIClient()
        first_token = RefreshToken.for_user(self.first_user)
        self.first_authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(first_token.access_token)}'
        )

        self.second_authorized_client = APIClient()
        second_token = RefreshToken.for_user(self.second_user)
        self.second_authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(second_token.access_token)}'
        )

    def test_create_like_by_guest(self):
        response = self.guest_client.post(
            f'/api/v1/news/{self.first_news.id}/likes/'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_like_by_authorized(self):
        response = self.first_authorized_client.post(
            f'/api/v1/news/{self.second_news.id}/likes/'
        )

        message = {'message': 'Лайк добавлен.'}

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), message)

    def test_create_existing_like(self):
        response = self.first_authorized_client.post(
            f'/api/v1/news/{self.first_news.id}/likes/'
        )

        message = {'error': 'Вы уже поставили лайк этой новости!'}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), message)

    def test_delete_like_by_guest(self):
        response = self.guest_client.delete(
            f'/api/v1/news/{self.first_news.id}/likes/'
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_like_by_author(self):
        response = self.first_authorized_client.delete(
            f'/api/v1/news/{self.first_news.id}/likes/'
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_unexisting_like(self):
        response = self.first_authorized_client.delete(
            f'/api/v1/news/{self.second_news.id}/likes/'
        )
        message = {'error': 'Вы не ставили лайк этой новости!!'}

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), message)
