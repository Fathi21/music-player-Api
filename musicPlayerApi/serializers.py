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
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'created_at' in data and hasattr(instance, 'created_at'):
            data['created_at'] = instance.created_at.date().isoformat() if instance.created_at else None
        return data

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
    SongID = serializers.PrimaryKeyRelatedField(queryset=Music.objects.all())
    UserId = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = SongsAddedToPlayList
        fields = ['SongID', 'UserId']
        
        

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'    
