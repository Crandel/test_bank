import StringIO
import json

from PIL import Image
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import InMemoryUploadedFile
from push_notifications.models import APNSDevice
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ebay.factories import ItemCategoryFactory
from users.factories import UserFactory
from users.serializers import SignUpSerializer
from users.views import ForgotPasswordView


def get_temporary_image():
    io = StringIO.StringIO()
    size = (200, 200)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(io, format='JPEG')
    image_file = InMemoryUploadedFile(io, None, 'foo.jpg', 'jpeg', io.len, None)
    image_file.seek(0)
    return image_file


User = get_user_model()


class TestSignInView(APITestCase):
    def setUp(self):
        super(TestSignInView, self).setUp()
        self.user = UserFactory.create()
        self.url = reverse("users:signin")

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
            'device_type': 'apns',
            'registration_id': 'registration_id'
        }
        expected_status_code = status.HTTP_200_OK

        response = self.client.post(self.url, request_data)
        # expected_result = UserSerializer(instance=self.user, context={'request': response.wsgi_request}).data
        self.assertEqual(response.status_code, expected_status_code)
        # self.assertEqual(json.loads(response.content), expected_result)

    def test_post_with_invalid_data(self):
        request_data = {
            'email': self.user.email,
            'password': 'incorrect_password',
            'device_type': 'apns',
            'registration_id': 'registration_id'
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST

        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

        request_data = {
            'email': 'incorrect_email',
            'password': 'test1234',
            'device_type': 'apns',
            'registration_id': 'registration_id'
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST

        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)


class TestSignUpView(APITestCase):
    def setUp(self):
        super(TestSignUpView, self).setUp()
        self.url = reverse('users:signup')

    def test_post(self):
        registration_id = '7407000434ebc7d9f5e7b4eac8f89cb3a9d4de300018b08c7cbd6b09beb16c7e'
        request_data = {
            'email': 'user_1@example.com',
            'password': 'test',
            'username': 'test',
            'device_type': 'apns',
            'registration_id': registration_id
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST
        expected_result = {
            'avatar': [u'No file was submitted.'],
            'password': [SignUpSerializer.default_error_messages['weak_password']]
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(json.loads(response.content), expected_result)

        request_data = {
            'avatar': get_temporary_image(),
            'email': 'user_1@example.com',
            'password': 'test1234',
            'username': 'test',
            'device_type': 'apns',
            'registration_id': registration_id
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APNSDevice.objects.all().count(), 1)

        request_data = {
            'avatar': get_temporary_image(),
            'email': 'user_3@example.com',
            'password': 'test1234',
            'username': 'test',
            'device_type': 'apns',
            'registration_id': registration_id
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APNSDevice.objects.all().count(), 1)

        request_data = {
            'avatar': get_temporary_image(),
            'email': 'user_4@example.com',
            'password': 'test1234',
            'username': 'test',
        }
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(APNSDevice.objects.all().count(), 1)


class TestForgotPasswordView(APITestCase):
    def setUp(self):
        super(TestForgotPasswordView, self).setUp()
        self.user = UserFactory.create()
        self.url = reverse("users:forgot_password")

    def test_incorrect_email(self):
        request_data = {
            'email': 'incorrect email'
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

        request_data = {
            'email': 'doesnotexist@gmail.com'
        }
        expected_status_code = status.HTTP_400_BAD_REQUEST
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

    def test_correct_email(self):
        request_data = {
            'email': self.user.email
        }
        expected_status_code = status.HTTP_200_OK
        response = self.client.post(self.url, request_data)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertContains(response, ForgotPasswordView.default_messages['success'].format(self.user.email))

        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Forgot Password')


class TestUserViewSet(APITestCase):
    def setUp(self):
        self.user = UserFactory.create()
        self.not_owner = UserFactory.create()
        self.basename = 'users'

    def test_get(self):
        url = reverse('users:{0}-{1}'.format(self.basename, 'list'))
        response = self.client.get(url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(response.status_code, expected_status_code)

        self.client.force_authenticate(self.user)
        url = reverse('users:{0}-{1}'.format(self.basename, 'list'))
        response = self.client.get(url)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(response.status_code, expected_status_code)

    def test_post(self):
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.post(url, request_data)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(response.status_code, expected_status_code)

        self.client.force_authenticate(self.user)
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.post(url, request_data)
        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, expected_status_code)

    def test_put(self):
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.put(url, request_data)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(response.status_code, expected_status_code)

        self.client.force_authenticate(self.user)
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.put(url, request_data)
        expected_status_code = status.HTTP_400_BAD_REQUEST
        self.assertEqual(response.status_code, expected_status_code)

        request_data = {
            'username': 'new_username',
            'password': '1234test',
            'email': 'new_email@example.com'
        }
        expected_status_code = status.HTTP_200_OK
        response = self.client.put(url, request_data)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertTrue(user.check_password('1234test'))
        self.assertTrue(user.username, 'new_username')
        self.assertTrue(user.email, 'new_email@example.com')

        self.client.force_authenticate(self.not_owner)
        request_data = {
            'username': 'new_username',
            'password': '1234test',
            'email': 'new_email@example.com'
        }
        expected_status_code = status.HTTP_403_FORBIDDEN
        response = self.client.put(url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

    def test_patch(self):
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.patch(url, request_data)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(response.status_code, expected_status_code)

        self.client.force_authenticate(self.user)
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.patch(url, request_data)
        expected_status_code = status.HTTP_200_OK
        self.assertEqual(response.status_code, expected_status_code)

        request_data = {
            'username': 'new_username',
            'password': '1234test',
            'email': 'new_email@example.com'
        }
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(url, request_data)
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(response.status_code, expected_status_code)
        self.assertTrue(user.check_password('1234test'))
        self.assertTrue(user.username, 'new_username')
        self.assertTrue(user.email, 'new_email@example.com')

        self.client.force_authenticate(self.not_owner)
        request_data = {
            'username': 'new_username',
            'password': '1234test',
            'email': 'new_email@example.com'
        }
        expected_status_code = status.HTTP_403_FORBIDDEN
        response = self.client.patch(url, request_data)
        self.assertEqual(response.status_code, expected_status_code)

        # Update Item Category
        category_1 = ItemCategoryFactory.create()
        category_2 = ItemCategoryFactory.create()
        self.client.force_authenticate(self.user)

        request_data = {
            'categories': [category_1.pk, category_2.pk],
        }
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(url, request_data)
        self.assertEqual(response.status_code, expected_status_code)
        user = User.objects.get(pk=self.user.pk)
        self.assertEquals(list(user.categories.all().values_list('pk', flat=True)), [category_1.pk, category_2.pk])

        category_3 = ItemCategoryFactory.create()
        self.client.force_authenticate(self.user)

        request_data = {
            'categories': [category_1.pk, category_3.pk],
        }
        expected_status_code = status.HTTP_200_OK
        response = self.client.patch(url, request_data)
        self.assertEqual(response.status_code, expected_status_code)
        user = User.objects.get(pk=self.user.pk)
        self.assertEquals(list(user.categories.all().values_list('pk', flat=True)), [category_1.pk, category_3.pk])

    def test_delete(self):
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.delete(url, request_data)
        expected_status_code = status.HTTP_403_FORBIDDEN
        self.assertEqual(response.status_code, expected_status_code)

        self.client.force_authenticate(self.user)
        url = reverse('users:{0}-{1}'.format(self.basename, 'detail'), kwargs={'pk': self.user.pk})
        request_data = {}
        response = self.client.delete(url, request_data)
        expected_status_code = status.HTTP_405_METHOD_NOT_ALLOWED
        self.assertEqual(response.status_code, expected_status_code)
