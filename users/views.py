from django.shortcuts import render
from users.models import User
from rest_framework.generics import CreateAPIView
from users.serializer import UserSerializer


# Create your views here.


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()