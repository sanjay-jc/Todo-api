from django.urls import path

#local imports

from .views import (
    List_todo,
    Create_todo,
    Delete_todo,
    Update_todo,
    Update_task_status
)


urlpatterns = [
    path('list-todo',List_todo.as_view(),name='list_todo'),
    path('create-todo',Create_todo.as_view(),name='create_todo'),
    path('delete-todo',Delete_todo.as_view(),name='delete_todo'),
    path('update-todo',Update_todo.as_view(),name='update_todo'),
    path('update-todo-task',Update_task_status.as_view(),name='update_todo_task'),
]