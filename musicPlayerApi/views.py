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
from django.db.models import Q
from django.contrib.auth.hashers import check_password

def Api(request):

    return JsonResponse({"Name" : "Fathi"})

# GET request for all songs list 
@api_view(['GET'])
def GetAllMusic(request):

    try:
        Musics = Music.objects.all()
        if request.method == 'GET':
            serializer = MusicSerializer(Musics, many=True)
            return Response(serializer.data)

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
        if request.method == 'GET':
            serializer = MusicSerializer(Musics, many=True)
            return Response(serializer.data)

    except Musics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


#Post request, Like a song by id
@api_view(['POST'])
def LikeASongById(request):
        
    if request.method == 'POST':
        
        serializer = LikeSerializer(data=request.data)

        if serializer.is_valid():
            songId = serializer.validated_data['SongID']
            userId = serializer.validated_data['UserId']
            like = Liked.objects.filter(Q(SongID=songId) & Q(UserId=userId))
            
            print('LIKE', like)

            if (like.count() < 1):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
                like.delete()
                return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


#Get request for likes by song id 
@api_view(['GET'])
def GetLikesBySongId(request, pk):

    try:
        Likes = Liked.objects.filter(SongID=pk)
        
        if request.method == 'GET':
            serializer = LikeSerializer(Likes, many=True)
            return Response(serializer.data)

    except Likes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def GetAllLikedSongs(request):
    try:
        likes = Liked.objects.all()
        if request.method == 'GET':
            serializer = LikeSerializer(likes, many=True)
            return Response(serializer.data)

    except likes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


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
                print(newUser)
                newUser.save()

                token = Token.objects.create(user = newUser)

                return Response(serialized.data, status=status.HTTP_201_CREATED)
            
            else:
                return Response(serialized.data, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login(request, username, password):
    try:
        user = User.objects.filter(username=username)

        if request.method == 'GET':
            if user:
                for dataRequested in user:
                    userPassword = dataRequested.password
                    userToken = Token.objects.get_or_create(user=dataRequested)

                checkPassword = check_password(password, userPassword)

                print(userToken[0])
                if (checkPassword and userToken):

                    content = {
                        'UserId': dataRequested.id,
                        'Username': dataRequested.username,
                        'Email': dataRequested.email,
                        'Token': str(userToken[0]),
                        'isUserHasToken': True

                    }
                    return Response(content)
                else:
                    content = {
                        'message' : 'Username or password is incorrect',
                        'isUserHasToken': False
                    }
                    return Response(content)
            else:
                content = {
                    'message' : 'Username or password is incorrect',
                    'isUserHasToken': False                
                }
                return Response(content)            
    except user.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def UserById(request, pk):
    try:
        Users = User.objects.filter(id=pk)
        if request.method == 'GET':
            serializer = UserSerializer(Users, many=True)
            return Response(serializer.data)

    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def UserByUserName(request, username):
    try:
        Users = User.objects.filter(username=username)
        if request.method == 'GET':
            serializer = UserSerializer(Users, many=True)
            return Response(serializer.data)

    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ExistUsers(request):
    try:
        Users = User.objects.all()
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExistUsersSerializer(Users, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def GetPlayList(request):
    
    allPlayList = PlayList.objects.all()

    if request.method == 'GET':
        serializer = PlayListSerializer(allPlayList, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def GetSongsAddedToPlayList(request):
    AllSongsAddedToPlayList = SongsAddedToPlayList.objects.all()

    if request.method == 'GET':
        serializer = SongsAddedToPlayListSerializer(AllSongsAddedToPlayList, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def CreateNewPlayListAddSong(request):

    serialized = SongsAddedToPlayListSerializer(data=request.data)
    if serialized.is_valid():

        if request.method == 'POST':
            breakpoint()
            song = serialized.validated_data['SongID']
            user = serialized.validated_data['UserId']

            songId = Music.objects.get(Title=song)
            userId = User.objects.filter(username=user)

            if songId and userId:

                AddSongToNewPlayList = SongsAddedToPlayList(
                    song=song,
                    user=user,
                )

                # newPlayList = PlayList(
                #     song=song,
                #     user=user,
                # )

                # AddSongToNewPlayList.save()

                print (AddSongToNewPlayList)

                return Response(serialized.data)




    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



