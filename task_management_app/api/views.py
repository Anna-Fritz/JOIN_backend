from rest_framework.views import APIView
from rest_framework import mixins
from rest_framework import generics
from ..models import User
from .serializers import UserSerializer


class UsersView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSingleView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
