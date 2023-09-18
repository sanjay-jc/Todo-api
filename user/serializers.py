from rest_framework.serializers import ModelSerializer,Serializer,CharField,ValidationError,EmailField
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from django.contrib.auth import get_user_model

User  = get_user_model()

class User_serializers(ModelSerializer):

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data) #this creates a object of the give user

        if password is not None:
            instance.set_password(password) 
        instance.save()
        return instance
        
    def update(self,instance,validate_data):
        '''
        this method is used to update the fields in the given user
        '''
        for attr,value in validate_data:
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance,attr,value) 
        instance.save()
        return instance
    
    
    class Meta:
        model = User
        extra_kwargs = {"password":{'write_only':True}}
        fields = ['email','password','first_name']




class Userlogin_serializer(Serializer):
    email = EmailField()
    password = CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise ValidationError('Invalid credentials')
        else:
            raise ValidationError('Username and password are required')

        data['user'] = user
        return data