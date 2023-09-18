from django.db import models
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
STATUS_CHOICE = (
   ( True,"Completed"),
    (False,"Pending")
)


class Status_manager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)

class Base_model(models.Model):
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now  = True)
    status =models.BooleanField(default = False,choices = STATUS_CHOICE)

    objects = models.Manager()
    is_active = Status_manager() # returns only the instance with  status completed

    class Meta:
        abstract = True


def is_user_owner(request_user, item_user):
    """
    Check if the request user is the owner of the item.
    """
    return request_user == item_user