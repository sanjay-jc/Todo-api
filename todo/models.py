from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.template.defaultfilters import slugify
# local imports 
from .utils import (
    Base_model,
)

User = get_user_model()

# Create your models here.

class Todo_model(Base_model):
    title = models.CharField(max_length = 500)
    description = models.TextField()
    created_by = models.ForeignKey(User,on_delete = models.CASCADE)
    slug_field = models.SlugField(max_length =100,null=True,blank=True)

    def save(self,*args,**kwargs):
        if not self.slug_field:
            self.slug_field = slugify(self.title[:50]+str(uuid4())[:20])
        super().save(*args,**kwargs)

    class Meta:
        ordering = ['-created_on']
        verbose_name_plural = "Todos"