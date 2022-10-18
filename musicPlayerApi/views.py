from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from .models import *
from .serializers import *
from django.contrib.auth.models import User

def Api(request):

    return JsonResponse({"Name" : "Fathi"})

# GET request for all songs list 
@api_view(['GET'])
def GetAllMusic(request):

    try:
        Musics = Music.objects.all()
    except Musics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(Musics)
    if request.method == 'GET':
        serializer = MusicSerializer(Musics, many=True)
        return Response(serializer.data)


# GET request by song id 
@api_view(['GET'])
def GetSongById(request, pk):

    try:
        Musics = Music.objects.filter(id=pk)
    except Musics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MusicSerializer(Musics, many=True)
        return Response(serializer.data)


#Post request, Like a song by id
@api_view(['POST'])
def LikeASongById(request, pk):

    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Get request for likes by song id 
@api_view(['GET'])
def GetLikesBySongId(request, pk):

    try:
        Likes = Liked.objects.filter(id=pk)
    except Likes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LikeSerializer(Likes, many=True)
        return Response(serializer.data)


#https://docs.amplication.com/docs/tutorials/react-todos/step-004/


@api_view(['POST'])
def Register(request):

    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():

        if request.method == 'POST':
            email = serialized.validated_data['email']
            username = serialized.validated_data['username']
            password = serialized.validated_data['password']

            newUser = User(
                username=username,
                email=email,
                password = make_password(password)
            )

            userExist = User.objects.filter(email=email)
            if not userExist:
                newUser.save()
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serialized.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):

    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        #serialized.save()

        return Response(serialized.data, status=status.HTTP_200)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def UserById(request, pk):
    try:
        Users = User.objects.filter(id=pk)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(Users, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def TokanForUser(request):
    try:
        for user in User.objects.all():
            tokenUsers = Token.objects.get_or_create(user=user)
    except tokenUsers.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(tokenUsers, many=True)
        return Response(serializer.data)


