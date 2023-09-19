from rest_framework.serializers import ModelSerializer,SerializerMethodField


#local imports

from .models import Todo_model


class Todo_list_serializer(ModelSerializer):

    '''list todo serializer '''
    user = SerializerMethodField()
    class Meta:
        model = Todo_model
        
        fields = ['title','description','user','status',"created_on",'slug_field']

    def get_user(self,obj):
        user_name=obj.created_by.get_user_name()
        return user_name

class Create_todo_serializer(ModelSerializer):
    class Meta:
        model = Todo_model
        fields = ['title','description']





        