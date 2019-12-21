
from django.contrib.auth import get_user_model, models
from django.shortcuts import render
from rest_framework import viewsets, permissions, views, response, status, authentication, generics
from todo.models import List, Profile
from todo.todoserializers import TodoSerializers, UserSerializers, UserRegistrationSerializers
from todo.forms.registerForm import SignupForm


class ListView(viewsets.ModelViewSet):
    queryset = List.objects.all()
    serializer_class = TodoSerializers
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class UserView(viewsets.ReadOnlyModelViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    # authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = UserSerializers
    queryset = Profile.objects.all()

    def get_object(self):
        return self.request.user

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializers
    queryset = Profile.objects.all()

class UserEmailVerificationView(views.APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, uidb64, token):
        activated_user = Profile.objects.activate_user(uidb64, token)
        if activated_user:
            return response.Response(status=status.HTTP_200_OK)
        return response.Response(status=status.HTTP_204_NO_CONTENT)
    

    
