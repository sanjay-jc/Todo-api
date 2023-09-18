from django.db import models
from django.contrib.auth.models import AbstractUser
from django.template.defaultfilters import slugify
from uuid import uuid4

#local imports
from .managers import Custom_user_manager
class Custom_user(AbstractUser):
    ''' custom user model with email as unique identifier '''
    username = None
    email = models.EmailField('Email Address',unique=True)
    slug_field = models.SlugField(max_length=60,null=True,blank=True,unique=True)

    def save(self,*args,**kwargs):
        if not self.slug_field:
            self.slug_field = slugify(str(uuid4())[:16])
        super().save(*args,**kwargs)
    
    def get_user_name(self):
        ''' return the first_name if avaiable else return the email'''
        if self.first_name:
            return self.first_name
        else:
            return self.email
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = Custom_user_manager()

    def __str__(self):
        return self.email