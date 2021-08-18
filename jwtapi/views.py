from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializer import RegisterSerializer, UserSerializer

# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password


import jwt
from Quizeal.settings import SIMPLE_JWT


class RegisterApi(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        try:
            request.POST._mutable = True
            request.data["password"] = make_password(
                request.data["password"], None, "md5"
            )
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            return Response(
                {
                    "status": 200,
                    "user": UserSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "detail": "Registered Successfully. Login to Quizeal",
                }
            )
        except:
            return Response({"status": "500", "detail": serializer.errors}, status=500)


class CustomJWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        credentials = {"username": "", "password": attrs.get("password")}
        user_obj = (
            User.objects.filter(email=attrs.get("username")).first()
            or User.objects.filter(username=attrs.get("username")).first()
        )

        if user_obj:
            credentials["username"] = user_obj.username

        return super().validate(credentials)


class LoadUserView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            decode = jwt.decode(
                request.data["token"],
                SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[SIMPLE_JWT["ALGORITHM"]],
            )

            if not decode:
                return Response(
                    {"status": "401", "detail": "Invalid Token"}, status=401
                )

            user = User.objects.get(id=decode["user_id"])

            if not user:
                return Response(
                    {"status": "401", "detail": "User does not exists"}, status=401
                )

            return Response(
                {
                    "status": "200",
                    "data": {
                        "token_type": decode["token_type"],
                        "user": model_to_dict(user),
                    },
                },
            )
        except:
            return Response(
                {"status": "500", "detail": "Internal Server Error"}, status=500
            )


# DONE
class ChangePassword(APIView):
    def post(self, request, *args, **kwargs):

        try:
            decode = jwt.decode(
                request.data["token"],
                SIMPLE_JWT["SIGNING_KEY"],
                algorithms=[SIMPLE_JWT["ALGORITHM"]],
            )
            user = User.objects.get(id=decode["user_id"])

            if user.username != request.data["username"]:
                return Response(
                    {"status": 401, "detail": "Token is Invalid!"}, status=401
                )

            if not check_password(request.data["old_password"], user.password):
                return Response(
                    {"status": 401, "detail": "Old Password Incorrect!"}, status=401
                )

            user.password = make_password(request.data["new_password"], None, "md5")
            user.save()

            return Response({"status": 200, "detail": "Password changed successfully!"})

        except:
            return Response(
                {"status": 500, "detail": "Internal Server Error"}, status=500
            )
