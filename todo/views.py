from django.views import View
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
import logging


logger = logging.getLogger(__name__)

#local imports 

from .models import (
    Todo_model,
    )

from .utils import (
    is_user_owner
)


from .serializers import (
    Todo_list_serializer,
    Create_todo_serializer,
)


from .tasks import (
    send_email_task
)

from .paginations import (
    Custom_pagination_response,
    )
class List_todo(APIView,Custom_pagination_response):
    
    '''  shows the todo of the login user, if not todo is found return a message '''
    def get(self,request,*args,**kwargs):
        try:
            todos = Todo_model.objects.filter(created_by = request.user)
            if todos:
                page = self.paginate_queryset(todos,request)
                serializer = Todo_list_serializer(instance=page,many=True)
                
                return self.get_paginated_response(serializer.data)

            else:
                return Response({"status":0,'message':"No todos found for this user","data":None},status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occured in list-todo: {str(e)}")
            return Response({
                'status':0,
                "message":str(e),
                'data':None
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Create_todo(APIView):
    ''' create a new todo '''
    def post(self,request,*args,**kwargs):
        
        try:
            serializer = Create_todo_serializer(data = request.data)
            if serializer.is_valid():
                serializer.save(created_by = request.user)
                return Response({
                    'status':1,
                    "message":"Todo added successfully",
                    "data":serializer.data
                },status=status.HTTP_201_CREATED)
            
            else:
                return Response({
                    'status':0,
                    'message':serializer.errors,
                    "data":None
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Error occured in create-todo: {str(e)}")
            return Response({
                'status':0,
                'message':str(e),
                'data':None
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Delete_todo(APIView):
    ''' delete a todo with given slug '''
    def delete(self,request,*args,**kwargs):
        try:
            todo_slug  = request.data.get('slug')
            if todo_slug:
                todo = Todo_model.objects.filter(slug_field = todo_slug).first()
                
                if todo:
                    is_verified = is_user_owner(todo.created_by,request.user)
                    if is_verified:
                        todo.delete()
                        return Response({
                            'status':1,
                            'message':"Todo deleted successfully",
                            'data':None
                        },status=status.HTTP_200_OK)
                    else:
                        return Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
                else:
                    return Response({
                        'status':0,
                        'message':"Todo does not exist",
                        "data":None

                    },status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                    'status':0,
                    'message':"Please provide todo slug to be deleted",
                    'data':None
                },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error occured in delete-todo: {str(e)}")
            return Response({
                    'status':0,
                    'message':"Internal server error",
                    'data':None
                },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Update_todo(APIView):
    def put(self, request,*args,**kwargs):
        try:
            todo = Todo_model.objects.get(slug_field=request.data.get('slug'))
        except Todo_model.DoesNotExist:
            return Response({
                'status': 0,
                'message': "Todo does not exist",
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        is_verified = is_user_owner(todo.created_by,request.user)
        if is_verified:
            serializer = Create_todo_serializer(todo, data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': 1,
                    'message': "Todo updated successfully",
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                logger.error(f"Error occured in delete-todo: {serializer.errors}")
                return Response({
                    'status': 0,
                    'message': serializer.errors,
                    'data': None
                }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
        

class Update_task_status(APIView):
    def post(self,request,*args,**kwargs):
        try:
            todo = Todo_model.objects.get(slug_field = request.data.get('slug'))
            is_verified = is_user_owner(todo.created_by,request.user)
            if is_verified:
                todo.status = not todo.status
                todo.save()
                print(todo.created_by.get_email(),'<<<<,')
                send_email_task.delay(todo.created_by.get_user_name(),todo.created_by.get_email(),f'{todo.title} changed to {"Completed" if todo.status else "Pending"}')
                return Response({
                    'status': 1,
                    'message': f'Status of todo changed successfully',
                    'data': None
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                            'status':0,
                            'message':"You are not authorized to perform this operation",
                            'data':None
                        },status=status.HTTP_403_FORBIDDEN)
        
        except Todo_model.DoesNotExist:
            logger.error(f"Todo does not exist ")
            return Response({
                'status': 0,
                'message': 'Todo does not exist',
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            logger.error(f"Error occured in delete-todo: {str(e)}")
            return Response({
                'status': 0,
                'message': str(e),
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)
