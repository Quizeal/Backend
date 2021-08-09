from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
# Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name','id',)    
        def create(self, validated_data):
            user = User.objects.create_user(validated_data['username'],password = validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])
            extra_kwargs = {
                'first_name': {'required': True},
                'last_name': {'required': True},
                'username': {'required': True},
                'password': {'required': True}
            }
            user.password=make_password(user.password)# User serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','id',)