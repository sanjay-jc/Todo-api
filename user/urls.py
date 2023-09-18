from django.urls import path

#local imports 

from .views import (
    LoginAPIView,
    Custom_user_register,
)

urlpatterns  = [
    path('register',Custom_user_register.as_view(),name='register'),
    path('login',LoginAPIView.as_view(),name='login'),
]