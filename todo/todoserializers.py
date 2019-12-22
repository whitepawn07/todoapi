from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from todo.models import List, Profile
from django.contrib.auth.models import User
import pdb
class TodoSerializers(serializers.HyperlinkedModelSerializer):
    
    class Meta(object):
        model = List
        fields = ('id', 'url', 'title', 'description', 'priority', 'is_done', 'created_by', 'created_at', 'updated_at')

class UserSerializers(serializers.HyperlinkedModelSerializer):
    class Meta(object):
        model = Profile
        fields = ( 'id', 'url', 'first_name', 'last_name', 'email', 'is_verified')
        
class UserRegistrationSerializers(serializers.ModelSerializer):

    class Meta(object):
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'password')

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email Already Exist.")
        return value
    
    def validate_password_2(self, value):
        data = self.get_initial()
        password = data.get('password')
        if password != value:
            raise serializers.ValidationError("Passwords doesn't match.")
        return value

    def create(self, validated_data):
        
        email = validated_data.get('email')
        password = validated_data.get('password')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        site = get_current_site(self.context['request'])

        user = Profile.objects.create_user(email, first_name, last_name, password, site, True)

        return user
        
# class UserLoginSerializer(serializers.ModelSerializer):

#     email = serializers.EmailField(
#         required=False,
#         allow_blank=True,
#         write_only=True,
#         label="Email Address"
#     )

#     token = serializers.CharField(
#         allow_blank=True,
#         read_only=True
#     )

#     password = serializers.CharField(
#         required=True,
#         write_only=True,
#         style={'input_type': 'password'}
#     )

#     class Meta(object):
#         model = User
#         fields = ['email', 'password', 'token']

#     def validate(self, data):
#         email = data.get('email', None)
#         password = data.get('password', None)

#         if not email and not username:
#             raise serializers.ValidationError("Please enter username or email to login.")

#         user = User.objects.filter(
#             Q(email=email)
#         ).exclude(
#             email__isnull=True
#         ).exclude(
#             email__iexact=''
#         ).distinct()

#         if user.exists() and user.count() == 1:
#             user_obj = user.first()
#         else:
#             raise serializers.ValidationError("This username/email is not valid.")

#         if user_obj:
#             if not user_obj.check_password(password):
#                 raise serializers.ValidationError("Invalid credentials.")

#         if user_obj.is_active:
#             token, created = Token.objects.get_or_create(user=user_obj)
#             data['token'] = token
#         else:
#             raise serializers.ValidationError("User not active.")

#         return data