from rest_framework import generics
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated


class RegisterApi(generics.GenericAPIView):

    serializer_class = RegisterSerializer
    #permission_classes = (IsAuthenticated)

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        #self.perform_create(serializer)
        print(User.objects.all().values_list())

        return Response({
            "user": UserSerializer(user,context=self.get_serializer_context()).data,
            "message": "Registered Successfully. Login to Quizeal",
        })