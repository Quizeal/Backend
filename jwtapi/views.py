from rest_framework import generics
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
# from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password

class RegisterApi(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):

        request.data['password'] = make_password(request.data['password'], None, 'md5')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()


        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "Registered Successfully. Login to Quizeal",
        })