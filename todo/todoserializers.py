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
        
