from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import status
import logging


logger = logging.getLogger(__name__)

User = get_user_model()


# local imports
from .serializers import User_serializers, Userlogin_serializer
from todo.models import (
    Todo_model,
)
# Create your views here.


class Custom_user_register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        register_serializer = User_serializers(data=request.data)
        if register_serializer.is_valid():
            new_user = register_serializer.save()
            if new_user:
                token = RefreshToken.for_user(new_user)
                return Response({
                    'status': 1,
                    'message': "Registration Successfull.",
                    # 'refresh_token':str(token),
                    # 'access_token':str(token.access_token),
                    'data':None
                },status=status.HTTP_201_CREATED)
        return Response({
            'status': 0,
            'message': register_serializer.errors,
            'data': None
        },status=status.HTTP_400_BAD_REQUEST)



class LoginAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            serializer = Userlogin_serializer(data=request.data)
            is_valid = serializer.is_valid()
            if is_valid:
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({
                    "status": 1,
                    "message": "Login Successful",
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            
            return Response({
                    'status':0,
                    "message":serializer.errors,
                    'data':None   
                },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"An error occured in the login : {str(e)}")
            return Response({
                'status':0,
                'message':"Internal Server Error",
                'data':None
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)

