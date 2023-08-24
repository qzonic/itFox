from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from main.models import News


User = get_user_model()


class TestNews(APITestCase):
    """ Test news logic. """

    @classmethod
    def setUpClass(cls):
        super(TestNews, cls).setUpClass()
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

    def setUp(self) -> None:
        self.guest_client = APIClient()

        self.first_authorized_client = APIClient()
        first_token = RefreshToken.for_user(self.first_user)
        self.first_authorized_client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {str(first_token.access_token)}'
        )

    def test_get_news_list_by_guest(self):
        news_count = News.objects.count()

        response = self.guest_client.get('/api/v1/news/')
        response_json = response.json()
        expected_keys = ['count', 'next', 'previous', 'results']

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response_json.keys()), expected_keys)
        self.assertEqual(response_json['count'], news_count)

        for news_result, news_db in zip(
                response_json['results'],
                (self.second_news, self.first_news)
        ):
            self.assertEqual(news_result['id'], news_db.id)
            self.assertEqual(news_result['header'], news_db.header)

    def test_get_specific_news_by_guest(self):
        response = self.guest_client.get(f'/api/v1/news/{self.first_news.id}/')

        response_json = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['id'], self.first_news.id)
        self.assertEqual(response_json['header'], self.first_news.header)

    def test_create_news_by_guest(self):
        data = {
            'header': 'Guest test header',
            'text': 'Test guest text'
        }
        response = self.guest_client.post('/api/v1/news/', data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_news_without_fields(self):
        message = {
            'header': ['This field is required.'],
            'text': ['This field is required.']
        }
        response = self.first_authorized_client.post('/api/v1/news/')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), message)

    def test_create_news_by_authorized(self):
        news_count = News.objects.count()
        data = {
            'header': 'Authorized test header',
            'text': 'Test authorized text'
        }
        response = self.first_authorized_client.post(
            '/api/v1/news/',
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            News.objects.count(),
            news_count + 1
        )

        response_json = response.json()

        self.assertEqual(response_json['header'], data['header'])
        self.assertEqual(response_json['text'], data['text'])
