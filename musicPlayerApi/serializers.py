from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields ='__all__' 


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Liked
        fields ='__all__' 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields ='__all__' 
