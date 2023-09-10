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
from django.contrib.auth import authenticate
from django.contrib.auth import login
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

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


# Post request, Like a song by id
@api_view(['POST'])
def LikeASongById(request):
    if request.method == 'POST':
        serializer = LikeSerializer(data=request.data)

        if serializer.is_valid():
            songId = serializer.validated_data['SongID']
            userId = serializer.validated_data['UserId']

            liked = Liked.objects.filter(
                Q(SongID=songId) & Q(UserId=userId)).first()

            if liked:
                liked.delete()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    """
    This function retrieves likes by song ID using a GET request.
    
    :param request: The request parameter is the HTTP request object that contains information about the
    current request, such as the request method (GET, POST, etc.), headers, and query parameters
    :param pk: The parameter `pk` in the `GetLikesBySongId` function represents the song ID. It is used
    to filter the `Liked` objects based on the song ID and retrieve all the likes associated with that
    song
    :return: The code is returning a response with the serialized data of the likes that match the given
    song id.
    """
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


@api_view(['GET'])
def GetAllLikedSongsByUser(request, pk):
    try:
        if request.method == 'GET':

            getlikesByUser = Liked.objects.filter(UserId=pk)

            serializer = LikeSerializer(getlikesByUser, many=True)
            return Response(serializer.data)

    except getlikesByUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def Register(request):
    serialized = UserSerializer(data=request.data)

    if serialized.is_valid():
        email = serialized.validated_data['email']
        username = serialized.validated_data['username']
        password = serialized.validated_data['password']

        user, created = User.objects.get_or_create(
            email=email, defaults={'username': username, 'password': make_password(password)})

        if created:
            Token.objects.create(user=user)
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "User with this email already exists."}, status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login(request, username, password):
    try:
        user = User.objects.filter(username=username)

        if request.method == 'GET':
            if user:
                for dataRequested in user:
                    userPassword = dataRequested.password
                    userToken, _ = Token.objects.get_or_create(
                        user=dataRequested)

                checkPassword = check_password(password, userPassword)

                if checkPassword and userToken:

                    content = {
                        'UserId': dataRequested.id,
                        'Username': dataRequested.username,
                        'Email': dataRequested.email,
                        'Token': str(userToken),
                        'isUserHasToken': True,
                        'successfullyLoggedIn':'Congratulations! You have successfully logged in to your account. Welcome back!'
                    }
                    
                    return Response(content)
                else:
                    content = {
                        'message': 'Username or password is incorrect',
                        'isUserHasToken': False
                    }
                    return Response(content)
            else:
                content = {
                    'message': 'Username or password is incorrect',
                    'isUserHasToken': False
                }
                return Response(content)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    """
    The above code defines several API views in Python using the Django REST framework for retrieving
    user and playlist data.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, query
    parameters, and the request body. It is used to handle and process the incoming request and generate
    a response accordingly
    :param pk: The parameter "pk" is typically used as a shorthand for "primary key" and is commonly
    used to refer to the unique identifier of a database record. In the context of the code you
    provided, "pk" is used as a parameter in the functions `GetUserById` and `GetPlay
    :return: The code is returning serialized data of users, playlists, or a specific user or playlist
    based on the request made.
    """
@api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def GetUserById(request, pk):
    try:
        user = User.objects.get(id=pk)
        if request.method == 'GET':
            serializer = UserNoneSensitiveInformationSerializer(user)
            return Response(serializer.data)

    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def UserByUserName(request, username):
    try:
        Users = User.objects.filter(username=username)
        if request.method == 'GET':
            serializer = UserNoneSensitiveInformationSerializer(
                Users, many=True)
            return Response(serializer.data)

    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def ExistUsers(request):
    try:
        Users = User.objects.all()

        if request.method == 'GET':
            serializer = UserNoneSensitiveInformationSerializer(
                Users, many=True)
            return Response(serializer.data)

    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


    """
    The GetPlayList function retrieves all PlayList objects and returns them as serialized data in
    response to a GET request.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, query
    parameters, and the request body
    :return: a response containing the serialized data of all the PlayList objects.
    """
@api_view(['GET'])
def GetPlayList(request):

    allPlayList = PlayList.objects.all()

    if request.method == 'GET':
        serializer = PlayListSerializer(allPlayList, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def GetPlayListById(request, pk):
    try:
        playlist = PlayList.objects.get(id=pk)
    except PlayList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PlayListSerializer(playlist)
        return Response(serializer.data)


    """
    The function retrieves all songs added to a playlist by their playlist ID and returns them as
    serialized data.
    
    :param request: The `request` parameter is an object that represents the HTTP request made by the
    client. It contains information such as the request method (GET, POST, etc.), headers, and query
    parameters
    :param pk: The "pk" parameter in the code represents the primary key of the playlist for which you
    want to retrieve the songs. It is used to filter the SongsAddedToPlayList objects based on the
    PlayListId
    :return: The code is returning a response containing serialized data of songs from a playlist with
    the given playlist ID.
    """
@api_view(['GET'])
def GetSongsAddedToPlayListById(request, pk):
    AllSongsAddedToPlayList = SongsAddedToPlayList.objects.filter(
        PlayListId=pk)

    song_ids = AllSongsAddedToPlayList.values_list('SongID', flat=True)

    songsFromPlayList = Music.objects.filter(id__in=song_ids)

    if request.method == 'GET':
        serializer = MusicSerializer(songsFromPlayList, many=True)
        return Response(serializer.data)
    


@api_view(['POST'])
def CreateNewPlayList(request):
    serialized = PlayListSerializer(data=request.data)
    if serialized.is_valid():
        if request.method == 'POST':
            playListName = serialized.validated_data['PlayListName']
            description = serialized.validated_data['Description']
            userId = serialized.validated_data['UserId']

            userId = User.objects.get(id=userId.id)

            playListNameExist = PlayList.objects.filter(
                PlayListName=playListName)

            if userId and playListNameExist.count() == 0:
                createNewPlayList = PlayList(
                    PlayListName=playListName,
                    Description=description,
                    UserId=userId,
                )

                createNewPlayList.save()

                # Serialize the newly created playlist data
                new_playlist_data = PlayListSerializer(createNewPlayList).data

                return Response(new_playlist_data, status=status.HTTP_201_CREATED)

    return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


 
    """
    The function `GetSongfromPlaylist` retrieves all songs added to a playlist and returns them as
    serialized data.
    
    :param request: The request object contains information about the current HTTP request, such as the
    request method (GET, POST, etc.), headers, and query parameters
    :param pk: The "pk" parameter in the GetSongfromPlaylist function represents the primary key of the
    playlist for which you want to retrieve the songs. It is used to filter the SongsAddedToPlayList
    objects based on the PlayListId field
    :return: The code is returning a response containing the serialized data of all the songs added to a
    playlist with the given playlist ID. If the playlist is not found, a 404 status code is returned.
    """
@api_view(['GET'])
def GetSongfromPlaylist(request, pk):
    try:
        # Get all songs added to the playlist
        AllSongsAddedToPlayList = SongsAddedToPlayList.objects.filter(PlayListId=pk)
        # Musics = Music.objects.filter(id == random_song.SongID)

        # Serialize and return the random song
        if request.method == 'GET':

            if AllSongsAddedToPlayList is None:
                return Response(status=status.HTTP_404_NOT_FOUND)
            

            serializer = SongsAddedToPlayListSerializer(AllSongsAddedToPlayList, many=True)
            return Response(serializer.data)

    except AllSongsAddedToPlayList.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    """
    This function adds a song to a playlist.
    
    :param request: The request object contains information about the HTTP request made to the API. It
    includes details such as the request method (e.g., POST), headers, and body
    :return: The code is returning a response with the serialized data if it is valid and has been saved
    successfully to the database. The status code returned is HTTP 201 Created. If the data is not
    valid, it returns a response with the serializer errors and a status code of HTTP 400 Bad Request.
    """
@api_view(['POST'])
def AddSongSongToThePlayList(request):
    
    if request.method == 'POST':
            serializer = SongsAddedToPlayListSerializer(data=request.data)
            if serializer.is_valid():
                # Save the validated data to the database
                data = serializer
                data.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['GET'])
def GetCategoryById(request, pk):
    try:
        getCategory = Category.objects.filter(id=pk)

        if request.method == 'GET':
            serializer = CategorySerializer(getCategory, many=True)
            return Response(serializer.data)

    except getCategory.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

