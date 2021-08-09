from rest_framework import serializers
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name','id')    

        def create(self, validated_data):
            User.objects.create_user(validated_data['username'],password = validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','id',)