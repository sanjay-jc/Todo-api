# TaskIt
## _API documentation_

API endpoints, request formats, and response formats

## Account API endpoints

### Register
creating  new account with email, first name and password
-  http://localhost/account/register
-  method: post
-  Request format
    ```sh
   {
    "email":"testuser@gmail.com",
    "password":"testuser123",
    "first_name":"your first name"
    }
    ```
- Response format
     ```sh
   {
    "status": 1,
    "message": "Registration Successfull",
    "data":""
    }
    ```
### Login
login with the registered email and password
-  http://localhost/account/login
-  method: post
-  Request format
    ```sh
   {
    "email":"testuser@gmail.com",
    "password":"testuser123"
    }
    ```
- Response format
     ```sh
   {
    "status": 1,
    "message": "Login Successful",
    "refresh": "refresh token",
    "access": "access token"
    }
    ```

### Token Refresh
Issue new access token when current access token is expired
-  http://localhost/token/refresh/
-  method: post
-  Request format
    ```sh
   {
    "refresh":"testuser@gmail.com",
    }
    ```
- Response format
     ```sh
    {
        "access": "new access token"
    }
    ```

# Todo API endpoints
### Create Todo
create new todo
-  http://localhost/todo/create-todo
-  method: post
-  Request format
    ```sh
   {
    "title":"Complete the todo api endpoints",
    "description":"Complete the todo apis with clear documentation and postman integrations "
    }
    ```
- Response format
     ```sh
        {
        "status": 1,
        "message": "Todo added successfully",
        "data": {
            "title": "Complete the todo api endpoints",
            "description": "Complete the todo apis with clear documentation and postman integrations"
                }
        }
    ```
    
### List Todos
 List todos created by the user
-  http://localhost/todo/create-todo
-  method: get
-  default pagesize is 10
-  Request format
    ```sh
   {
    
    }
    ```
- Response format
     ```sh
    {{
        "next": next_page_url,
        "prev": previous_page_url,
        "status": 1,
        "message": "success",
        "data": [
                {
                    "title": "Complete the todo api endpoints",
                    "description": "Complete the todo apis with clear documentation and postman ",
                    "user": "sanjay@email.com",
                    "status": true,
                    "slug_field": "complete-the-todo-api-endpoints9e05da13-910e-428a-a"
                },
                {
                    "title": "4th todo in the list",
                    "description": "hello world",
                    "user": "sanjay@email.com",
                    "status": false,
                    "slug_field": "4th-todo-in-the-list-80815b6-bc94-4bd3-a"
                },
    ```
### Update Todo
 Update todo created by the user
-  http://localhost/todo/update-todo
-  method: put
-  Request format
    ```sh
        {
            "slug":"complete-the-todo-api-endpointsd0ce2732-4f08-462d-9",
            "title":"This is the and update to the existing endpoints",
            "description":"This is the updated to do with latest description"
        }
    ```
- Response format
     ```sh
           {
            "status": 1,
            "message": "Todo updated successfully",
            "data": {
                        "title": "This is the and upate to the existing endpoints",
                        "description": "This is the updated to do with latest description"
                }
            }
               
    ```

### Delete Todo
 Update todo created by the user
-  http://localhost/todo/delete-todo
-  method: delete
-  Request format
    ```sh
        {
            "slug":"complete-the-todo-api-endpointsd0ce2732-4f08-462d-9",
        }
    ```
- Response format
     ```sh
           {
                "status": 1,
                "message": "Todo deleted successfully",
                "data": null
            }
               
    ```
    
    
### Update Todo Status
 Update status of todo created by the user
-  http://localhost/todo/update-todo-task
-  once the status of the todo is changed and email is send to the user with the current status of todo
-  method: post
-  Request format
    ```sh
        {
            "slug":"complete-the-todo-api-endpointsd0ce2732-4f08-462d-9",
        }
    ```
- Response format
     ```sh
           {
            "status": 1,
            "message": "Status of todo changed successfully",
            "data": null
            }
               
    ```

