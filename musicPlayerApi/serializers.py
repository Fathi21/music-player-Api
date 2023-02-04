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
            'password'
        )

class ExistUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'email',
            'username',
        )


class PlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayList
        fields ='__all__' 


class SongsAddedToPlayListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SongsAddedToPlayList
        fields ='__all__' 