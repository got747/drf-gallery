from django.test import Client, TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser

from rest_framework import status
from rest_framework.test import APITestCase

from .views import get_user
from .models import User
from .serializers import UserRegistrSerializer, UserSerializer


class UserRegistrSerializerTestCase(APITestCase):

    def setUp(self):
        self.valid_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password'
        }

    def test_valid_data(self):
        serializer = UserRegistrSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_password_write_only(self):
        serializer = UserRegistrSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.check_password('password'))
        with self.assertRaises(AttributeError):
            serializer.data['password']


class UserSerializerTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='testuser@example.com',
                                        password='password')

    def test_valid_serialization(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['email'], 'testuser@example.com')
        self.assertEqual(serializer.data['username'], 'testuser')
        self.assertFalse(serializer.data['is_admin'])

    def test_valid_deserialization(self):
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'is_admin': True
        }
        serializer = UserSerializer(instance=self.user,
                                    data=data,
                                    partial=True)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newusername')
        self.assertEqual(self.user.email, 'newemail@example.com')
        self.assertTrue(self.user.is_admin)


class UserModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        email='testuser@example.com',
                                        password='password')

    def test_user_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'testuser@example.com')

    def test_is_admin(self):
        self.assertFalse(self.user.is_admin)

        self.user.is_admin = True
        self.user.save()

        self.assertTrue(self.user.is_admin)


class RegisterUserViewTestCase(APITestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = '/api/auth/register/'

    def test_register_user(self):
        data = {
            'email': 'testuser@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'testuser@email.com')
        self.assertTrue(User.objects.get().check_password('testpassword'))

    def test_register_user_with_existing_email(self):
        data = {
            'email': 'testuser@email.com',
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

        response = self.client.post(self.register_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)


class GetUserTestCase(APITestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create(username='testuser',
                                        email='testuser@example.com',
                                        password='testpassword')

    def test_get_user_authenticated(self):
        request = self.factory.get('/api/auth/get_user/')
        request.user = self.user

        response = get_user(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['is_admin'], self.user.is_admin)

    def test_get_user_unauthenticated(self):
        request = self.factory.get('/api/auth/get_user/')
        request.user = AnonymousUser()

        response = get_user(request)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
