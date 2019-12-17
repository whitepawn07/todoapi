from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import List
from django.contrib.auth.models import User
from .todoserializers import TodoSerializers, UserSerializers

class ListView(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = TodoSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
