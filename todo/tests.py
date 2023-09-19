from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
#local imports

from .models import (
    Todo_model
)


User = get_user_model()

class Todo_test(TestCase):
    ''' to check for creating a todo '''
    def setUp(self):
        self.user = User.objects.create_user(email='tester@email.com', password='adminuser123')
        self.todo = Todo_model.objects.create(
            title='This is a test todo',
            description='This is just a todo for testing',
            created_by=self.user,
        )

    def test_todo_creation(self):
        self.assertEqual(self.todo.title, 'This is a test todo')
        self.assertEqual(self.todo.description, 'This is just a todo for testing')
        self.assertEqual(self.todo.created_by, self.user)

    def test_ordering(self):
        # Create more todos with different created_on values
        todo_1 = Todo_model.objects.create(
            title='Todo 1',
            description='This is the first todo',
            created_by=self.user,
        )
        todo_2 = Todo_model.objects.create(
            title='Todo 2',
            description='This is the second todo',
            created_by=self.user,
        )

        # Query the database and check if the ordering is correct
        todos = Todo_model.objects.all()
        self.assertEqual(todos[0], todo_2)
        self.assertEqual(todos[1], todo_1)

    def test_verbose_name_plural(self):
        self.assertEqual(str(Todo_model._meta.verbose_name_plural), "Todos")



class List_todo_test(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='testuser@email.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.token = RefreshToken.for_user(self.user).access_token
        self.list_todo = reverse("list_todo")

    def test_show_todo(self):
        Todo_model.objects.create(created_by=self.user, title='Todo 1', description='Description 1')
        Todo_model.objects.create(created_by=self.user, title='Todo 2', description='Description 2')
        
        response = self.client.get(self.list_todo)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2) 

    def test_show_todos_with_no_existing_todos(self):
        response = self.client.get(self.list_todo)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_show_todo_invalid_user(self):
        self.user1 = User.objects.create_user(email='testuser1@email.com', password='testpassword')
        Todo_model.objects.create(created_by=self.user1, title='Todo 1', description='Description 1')
        Todo_model.objects.create(created_by=self.user1, title='Todo 2', description='Description 2')

        response = self.client.get(self.list_todo)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Test_create_todo(APITestCase):

    def setUp(self):
        self.create_url = reverse('create_todo')
        self.user = User.objects.create_user(email='testuser@email.com', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.token = RefreshToken.for_user(self.user).access_token

    def test_create_todo(self):
        self.valid_todo_data = {
            'title': 'Test Todo',
            'description': 'This is a test todo.',
            'completed': False,
        }
        response = self.client.post(self.create_url, self.valid_todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_todo_missing_fields(self):
        self.valid_todo_data = {
            'title': 'Test Todo',
            'completed': False,
        }
        response = self.client.post(self.create_url, self.valid_todo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Test_delet_todo(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@email.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(email='otheruser@email.com', password='otherpassword')
        self.client.force_authenticate(user=self.user)
        self.token = RefreshToken.for_user(self.user).access_token
        self.todo_data = {
            'title': "title",
            'description': "description",
            'status': True,
            'slug_field': 'test-slug',  # Assuming you have a slug value
        }

        self.todo = Todo_model.objects.create(created_by = self.user,**self.todo_data)
        self.delete_url = reverse('delete_todo') 


    def test_delete_own_todo(self):
        # Include the slug in request.data for deletion
        delete_data = {'slug': self.todo.slug_field}

        response = self.client.delete(self.delete_url, data=delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertFalse(Todo_model.objects.filter(slug_field=self.todo.slug_field).exists())

    def test_prevent_delete_other_user_todo(self):
        self.other_user_todo = Todo_model.objects.create(created_by = self.user,**self.todo_data)
        
        delete_data = {'slug': self.other_user_todo.slug_field}

        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(self.delete_url, data=delete_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Todo_model.objects.filter(slug_field=self.other_user_todo.slug_field).exists())


class Test_update_todo(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@email.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(email='otheruser@email.com', password='otherpassword')
        self.client.force_authenticate(user=self.user)
        self.token = RefreshToken.for_user(self.user).access_token
        self.todo_data = {
            'title': "title",
            'description': "description",
            'status': True,
            'slug_field': 'test-slug',  # Assuming you have a slug value
        }

        self.todo = Todo_model.objects.create(created_by = self.user,**self.todo_data)
        self.update_url = reverse('update_todo') 


    def test_update_todo(self):
        updated_data = {'slug': self.todo.slug_field,"title":"New title","description":"latest description"}
        response = self.client.put(self.update_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_missing_fields(self):
        updated_data = {"title":"New title","description":"latest description"}
        response = self.client.put(self.update_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_prevent_dupdate_other_user_todo(self):
        todo_data1 = {
            'title': "title",
            'description': "description",
            'status': True,
            'slug_field': 'test-slug1',  # Assuming you have a slug value
        }
        self.other_user_todo = Todo_model.objects.create(created_by = self.user,**todo_data1)
        
        updated_data = {'slug': self.todo.slug_field,"title":"New title","description":"latest description"}

        self.client.force_authenticate(user=self.other_user)

        response = self.client.put(self.update_url, data=updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Todo_model.objects.filter(slug_field=self.other_user_todo.slug_field).exists())



class Test_update_todo(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(email='testuser@email.com', password='testpassword')
        self.other_user = get_user_model().objects.create_user(email='otheruser@email.com', password='otherpassword')
        self.client.force_authenticate(user=self.user)
        self.token = RefreshToken.for_user(self.user).access_token
        self.todo_data = {
            'title': "title",
            'description': "description",
            'status': True,
            'slug_field': 'test-slug',  # Assuming you have a slug value
        }

        self.todo = Todo_model.objects.create(created_by = self.user,**self.todo_data)
        self.update_url = reverse('update_todo_task') 


    def test_update_todo(self):
        updated_data = {'slug': self.todo.slug_field}
        response = self.client.post(self.update_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_todo_missing_fields(self):
        updated_data = {}
        response = self.client.post(self.update_url, data=updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_prevent_update_status_other_user_todo(self):
        todo_data1 = {
            'title': "title",
            'description': "description",
            'status': True,
            'slug_field': 'test-slug1',  # Assuming you have a slug value
        }
        self.other_user_todo = Todo_model.objects.create(created_by = self.user,**todo_data1)
        
        updated_data = {'slug': self.todo.slug_field}
        self.client.force_authenticate(user=self.other_user)

        response = self.client.post(self.update_url, data=updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Todo_model.objects.filter(slug_field=self.other_user_todo.slug_field).exists())
