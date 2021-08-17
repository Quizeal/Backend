from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','password','username','first_name', 'last_name','id')    

    def validate_email(self,value):
            if User.objects.filter(email=value).exists():
                raise serializers.ValidationError("Email Already Exists,use another one")
            return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ('email','password','username','first_name','last_name','id')
