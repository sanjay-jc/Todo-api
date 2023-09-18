from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

class Custom_user_test(TestCase):
    def setUp(self):
        self.user_data = {
            "email":"tester@gmail.com",
            "password":"helloworld",
            "first_name":"Tester"

        }

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertTrue(user.first_name,self.user_data['first_name'])

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(**self.user_data)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)


    def test_user_str_representation(self):
        User = get_user_model()
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['email'])



class User_registration_apitest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('register')
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }

    def test_user_registration_view_success(self):
        response = self.client.post(self.registration_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_registration_view_invalid_data(self):
        invalid_data = {
            'email': 'invalid_email',
            'password': 'short',
        }
        response = self.client.post(self.registration_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class User_login_apitest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user_data = {
            'email': 'testuser@email.com',
            'password': 'testpassword',
        }
        self.user = get_user_model().objects.create_user(**self.user_data)

    def test_user_login_success(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_invalid_credentials(self):
        invalid_data = {
            'email': 'testuser',
            'password': 'invalid_password',
        }
        response = self.client.post(self.login_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)