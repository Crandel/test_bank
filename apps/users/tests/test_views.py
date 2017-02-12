import json
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.factories import UserFactory
from users.serializers import SignUpSerializer


User = get_user_model()


class TestSignInView(APITestCase):
    def setUp(self):
        super(TestSignInView, self).setUp()
        self.user = UserFactory.create()
        self.url = reverse("users:login")

    def test_get(self):
        """
        Test method get for SignUp view.
        Method get not allowed
        """
        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, expected_status_code)

    def test_post_with_valid_data(self):
        request_data = {
            'email': self.user.email,
            'password': 'test1234',
        }
        expected_status_code = status.HTTP_200_OK

        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

    def test_post_with_invalid_data(self):
        request_data = {
            'email': self.user.email,
            'password': 'incorrect_password',
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST

        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)


class TestSignUpView(APITestCase):
    def setUp(self):
        super(TestSignUpView, self).setUp()
        self.url = reverse('users:signup')

    def test_post(self):
        request_data = {
            'email': 'user_1@example.com',
            'password': 'test',
            'username': 'test',
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_result = {
            'password': [SignUpSerializer.default_error_messages['weak_password']]
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(json.loads(response.content), expected_result)

        request_data = {
            'email': 'user_1@example.com',
            'password': 'test1234',
            'username': 'test',
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request_data = {
            'email': 'user_3@example.com',
            'password': 'test1234',
            'username': 'test',
            'device_type': 'apns',
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        request_data = {
            'email': 'user_4@example.com',
            'password': 'test1234',
            'username': 'test',
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
