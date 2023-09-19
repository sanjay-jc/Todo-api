# TaskIt

TaskIt is a powerful API for managing your to-do tasks. It offers full CRUD (Create, Read, Update, Delete) functionality, secure authentication, and authorization via JWT tokens. Plus, it keeps you informed by sending email notifications when task statuses change.

## Key Features:

- **User Authentication**: Users can register, log in, and obtain JWT tokens for secure API access.
- **Task Management**: Create, retrieve, update, and delete to-do tasks effortlessly.
- **Authorization**: Ensure that only authorized users can access and manipulate their tasks.
- **Status Change Notifications**: Receive email notifications when the status of a to-do task changes.
- **User-Friendly**: Provides a user-friendly interface for seamless task management.
  With TaskIt, you can efficiently organize and track your to-do tasks while enjoying the benefits of robust authentication, authorization, and notifications.

## Technologies and tools used

- **Server**: Django
- **Primary database**: SQLite3
- **Temporary data store**: Redis
- **Message broker** : Rabbitmq
- **Task-queue**: Celery
- **Authentication**: JWT
- **API Framework**: Django REST Framework (DRF)

## Authentication API

- **Register API**: User can create a new account with email and password.
- **Login API**: Users can authenticate and obtain a JWT (JSON Web Token).
- **Refresh API**: Refreshes the JWT token and provides a new token to the user.

## CRUD APIs

- **Create API**: Allows users to create a new todo by providing the title and description.
- **List API**: List the details of the todos, including their title, description, and status, of the logged-in user.
- **Update API**: Allows users to update the information of an existing todo. The API returns the updated snippet details as a response.
- **Delete API**: Enables users to delete selected todo.
- **Status Update API**: The API updates the status of the todo, and also sends a notification to the user when the status changes.

# Installation and Setup

To run the TaskIt locally, follow these steps:

### Clone the GitHub repository:

     https://github.com/sanjayjc97/Todo-api.git

### Navigate to the project directory

     cd Todo-api

### Create a virtual environment:

     virtualenv venv

### Activate the virtual environment:

     source venv/bin/activate

### Install the required dependencies:

     pip install -r requirements.txt

### Install Rabbitmq and start the server :

     sudo apt-get install rabbitmq-server
     sudo systemctl start rabbitmq-server

### Apply the database migrations:

     python manage.py makemigrations

### Apply the database migrations:

     python manage.py migrate

### Start the development server:

     python manage.py runserver

### Start celery (use another instance of the terminal to run celery):

     celery -A core  worker -l info

### Start celery flower (use another instance of the terminal to run celery):

    celery -A core flower
    
### run celery flower to see the tasks:

    http://localhost:5555/

### Start Redis (use another instance of the terminal to run celery):

    redis-server

### To view results (use another instance of the terminal to run celery):

    redis-cli

### To view all results ( in redis-cli):

    > KEYS "*"

### To view details of a result (in redis-cli):

    > MGET "key_id"

## Running Tests

- [Test Docs](https://github.com/sanjayjc97/Todo-api/blob/master/TaskIt.md)

## API Documentation

- [API Documentation](https://github.com/sanjayjc97/Todo-api/blob/master/Api%20documentation%20.md)

## Postman Environment

- [Postman Environment](https://github.com/sanjayjc97/Todo-api/blob/master/Todo%20environments.postman_environment.json)

## Postman Collections

- [Postman Collections](https://github.com/sanjayjc97/Todo-api/blob/master/Todo-api.postman_collection.json)
