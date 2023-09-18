from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
#local imports

from .models import (
    Todo_model
)
# Create your tests here.
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


class TodoActionsTestCase(TestCase):
    '''test for listing the todos '''
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='testuser@email.com', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_show_todos_with_existing_todos(self):
        # Create some Todo_model objects for the user
        Todo_model.objects.create(created_by=self.user, title='Todo 1', description='Description 1')
        Todo_model.objects.create(created_by=self.user, title='Todo 2', description='Description 2')

        response = self.client.get('/todo/list-todo')  # Replace with your actual API URL

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['data']), 2)  # Ensure the correct number of todos is returned


    def test_show_todos_with_no_existing_todos(self):
        response = self.client.get('/todo/list-todo') # Replace with your actual API URL

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

