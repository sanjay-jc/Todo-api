from django.contrib import admin

#local imports
from .models import Todo_model

# Register your models here.

@admin.register(Todo_model)
class Todo_admin(admin.ModelAdmin):
    list_display = ["title","created_by","created_on","updated_on"]
