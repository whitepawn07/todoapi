from rest_framework import serializers
from todo.models import List
from django.contrib.auth.models import User

class TodoSerializers(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = List
        fields = ('id', 'url', 'title', 'description', 'priority', 'is_done', 'created_by', 'created_at', 'updated_at')

class UserSerializers(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ( 'id', 'url', 'first_name', 'last_name')

