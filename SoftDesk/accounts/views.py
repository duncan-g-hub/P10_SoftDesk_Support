from django.shortcuts import render
from rest_framework import viewsets


from accounts.models import User
from accounts.serializers import UserSerializer



class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
