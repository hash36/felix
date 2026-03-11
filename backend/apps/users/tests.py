from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class TokenAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='alice',
            email='alice@example.com',
            password='password123',
        )

    def test_can_obtain_token_with_valid_credentials(self):
        response = self.client.post(
            '/auth/token/',
            {'username': 'alice', 'password': 'password123'},
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())


class UserRegistrationTests(APITestCase):
    _VALID_PAYLOAD = {
        'username': 'bob',
        'email': 'bob@example.com',
        'first_name': 'Bob',
        'last_name': 'Smith',
        'password': 'securepass123',
    }

    def test_can_register_and_receives_token(self):
        response = self.client.post('/users/', self._VALID_PAYLOAD, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token', response.json())

    def test_registration_requires_email(self):
        payload = {**self._VALID_PAYLOAD, 'email': ''}

        response = self.client.post('/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_requires_username(self):
        payload = {**self._VALID_PAYLOAD, 'username': ''}

        response = self.client.post('/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_requires_first_name(self):
        payload = {**self._VALID_PAYLOAD, 'first_name': ''}

        response = self.client.post('/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_requires_last_name(self):
        payload = {**self._VALID_PAYLOAD, 'last_name': ''}

        response = self.client.post('/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_email_must_be_unique(self):
        self.client.post('/users/', self._VALID_PAYLOAD, format='json')

        response = self.client.post('/users/', self._VALID_PAYLOAD, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_must_be_unique(self):
        self.client.post('/users/', self._VALID_PAYLOAD, format='json')

        payload = {
            **self._VALID_PAYLOAD,
            'email': 'bob2@example.com',
        }
        response = self.client.post('/users/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
