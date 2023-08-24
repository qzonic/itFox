from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import News, Comment


User = get_user_model()


class TestComments(APITestCase):
    """ Test comment logic. """

    @classmethod
    def setUpClass(cls):
        super(TestComments, cls).setUpClass()
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
        cls.first_comment_for_first_news = Comment.objects.create(
            author=cls.first_user,
            news=cls.first_news,
            text='Test text for first news by first user',
        )
        cls.second_comment_for_first_news = Comment.objects.create(
            author=cls.second_user,
            news=cls.first_news,
            text='Test text for first news by second user',
        )
        cls.first_comment_for_second_news = Comment.objects.create(
            author=cls.first_user,
            news=cls.second_news,
            text='Test text for second news by first user',
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

    def test_get_comment_list_by_guest(self):
        comments_count = Comment.objects.filter(news=self.first_news).count()
        response = self.guest_client.get(
            f'/api/v1/news/{self.first_news.id}/comments/'
        )

        response_json = response.json()
        expected_keys = ['count', 'next', 'previous', 'results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_json.keys()), expected_keys)
        self.assertEqual(response_json['count'], comments_count)

        for comment in response_json['results']:
            self.assertTrue(Comment.objects.filter(
                author__id=comment['author']['id'],
                news__header=comment['news'],
                text=comment['text'],
            ).exists())

    def test_get_specific_comment_by_guest(self):
        response = self.guest_client.get(
            '/api/v1/news/{0}/comments/{1}/'.format(
                self.first_news.id,
                self.first_comment_for_first_news.id
            )
        )

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json['id'],
            self.first_comment_for_first_news.id
        )
        self.assertEqual(
            response_json['text'],
            self.first_comment_for_first_news.text
        )

    def test_create_comment_by_guest(self):
        data = {
            'text': 'Test guest text'
        }
        response = self.guest_client.post(
            f'/api/v1/news/{self.first_news.id}/comments/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_comment_without_fields(self):
        message = {'text': ['This field is required.']}
        response = self.first_authorized_client.post(
            f'/api/v1/news/{self.first_news.id}/comments/'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), message)

    def test_create_comment_by_authorized(self):
        comment_count = Comment.objects.count()
        data = {
            'text': 'Test authorized text'
        }
        response = self.first_authorized_client.post(
            f'/api/v1/news/{self.first_news.id}/comments/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            Comment.objects.count(),
            comment_count + 1
        )

        response_json = response.json()

        self.assertEqual(response_json['text'], data['text'])

    def test_delete_comment_by_another_user(self):
        response = self.second_authorized_client.delete(
            '/api/v1/news/{0}/comments/{1}/'.format(
                self.first_news.id,
                self.first_comment_for_first_news.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_comment_by_author(self):
        response = self.first_authorized_client.delete(
            '/api/v1/news/{0}/comments/{1}/'.format(
                self.first_news.id,
                self.first_comment_for_first_news.id
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
