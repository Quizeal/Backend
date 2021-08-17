from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.forms.models import model_to_dict


import jwt
from Quizeal.settings import SIMPLE_JWT 

class RegisterApi(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        request.POST._mutable = True
        request.data['password'] = make_password(request.data['password'], None, 'md5')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "status" : 200,
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "Registered Successfully. Login to Quizeal",
        })


class LoadView(APIView):

    def post(self,request,*args,**kwargs):
        try:
            decode = jwt.decode(request.data['token'], SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
            user = User.objects.get(id=decode['user_id'])

            res = {
                "status": "200",
                "data": {
                "token_type": decode["token_type"],
                "user": model_to_dict(user)
                }
            }
            return Response(res, status=200)
        except:
            res = {
                "status": "400",
                "error": "Bad Request"
            }
            return Response(res, status=400)

class ChangePassword(APIView):

    def post(self,request,*args,**kwargs):

        try:
            decode = jwt.decode(request.data['token'], SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
            user = User.objects.get(id=decode['user_id'])
            
            user.password = make_password(request.data['password'], None, 'md5')
            user.save()
            return Response({"msg": "Password changed successfully!"}, status = 200)

        except:
            return Response({"msg" : "Bad request"}, status = 400)
            