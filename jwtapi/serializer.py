from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name', 'last_name','id', 'email')    

        def create(self, validated_data):
            User.objects.create_user(validated_data['username'],password = validated_data['password'],first_name=validated_data['first_name'],last_name=validated_data['last_name'], email=validated_data['email'])


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password','first_name','last_name','id', 'email')
