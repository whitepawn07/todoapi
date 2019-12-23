from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
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
        
class UserLoginSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        write_only=True,
        label="Email Address"
    )

    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    token = serializers.CharField(
        allow_blank=True,
        read_only=True
    )

    class Meta(object):
        model = Profile
        fields = ['email', 'password','token']

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        if not email:
            raise serializers.ValidationError("Please enter email to login.")

        user = Profile.objects.filter(
            email=email
        ).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise serializers.ValidationError("This email is not valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if not user_obj.is_verified and not user_obj.is_admin:
            raise serializers.ValidationError("User not active.")
        else:
            token = RefreshToken.for_user(user_obj)
            data['token'] = 'Bearer '+str(token)
        
        return data