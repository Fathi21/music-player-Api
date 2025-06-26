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
        musics = Music.objects.all()
        serializer = MusicSerializer(musics, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Music.DoesNotExist:
        return Response({"error": "No music found"}, status=status.HTTP_404_NOT_FOUND)


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
def GetPlayListById(request, pk):
    """
    Retrieve a playlist by its ID.
    """
    try:
        playlist = PlayList.objects.get(id=pk)
        if request.method == 'GET':
            serializer = PlayListSerializer(playlist)
            return Response(serializer.data, status=status.HTTP_200_OK)
    except PlayList.DoesNotExist:
        return Response({"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def GetSongsAddedToPlayList(request):
    AllSongsAddedToPlayList = SongsAddedToPlayList.objects.all()

    if request.method == 'GET':
        serializer = SongsAddedToPlayListSerializer(AllSongsAddedToPlayList, many=True)
        return Response(serializer.data)


@api_view(['POST'])
def CreateNewPlayListAddSong(request):
    serializer = SongsAddedToPlayListSerializer(data=request.data)
    if serializer.is_valid():
        song = serializer.validated_data['SongID']
        user = serializer.validated_data['UserId']
        playlist_id = request.data.get('PlayListId')
        create_new = request.data.get('createNew', False)
        custom_name = request.data.get('name')
        custom_description = request.data.get('description', "User-created playlist")

        if create_new:
            # Create a new playlist with custom name and description
            playlist = PlayList.objects.create(
                PlayListName=custom_name or f"{user.username}'s Playlist",
                Description=custom_description,
                UserId=user,
                PhotoCover=None
            )
        elif playlist_id:
            try:
                playlist = PlayList.objects.get(id=playlist_id, UserId=user)
            except PlayList.DoesNotExist:
                return Response({"message": "Playlist not found for this user."}, status=status.HTTP_404_NOT_FOUND)
        else:
            # fallback (optional default playlist)
            playlist = PlayList.objects.filter(UserId=user).first()
            if not playlist:
                playlist = PlayList.objects.create(
                    PlayListName=f"{user.username}'s Playlist",
                    Description="Auto-generated playlist",
                    UserId=user,
                    PhotoCover=None
                )

        # Always allow adding song to playlist (even duplicates in other playlists)
        if SongsAddedToPlayList.objects.filter(PlayListId=playlist, SongID=song).exists():
            return Response({"message": "Song already exists in this playlist"}, status=status.HTTP_400_BAD_REQUEST)

        SongsAddedToPlayList.objects.create(
            PlayListId=playlist,
            UserId=user,
            SongID=song
        )

        return Response({
            "message": "Song added successfully",
            "playlist": {
                "id": playlist.id,
                "name": playlist.PlayListName,
                "description": playlist.Description
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def GetSongsInPlaylistById(request, pk):
    """
    Retrieve all songs in a playlist by playlist ID.
    """
    try:
        playlist = PlayList.objects.get(id=pk)
    except PlayList.DoesNotExist:
        return Response({"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND)

    songs_in_playlist = SongsAddedToPlayList.objects.filter(PlayListId=playlist)
    serializer = SongsAddedToPlayListSerializer(songs_in_playlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def RemoveSongFromPlaylist(request, playlist_id, song_id):
    """
    Remove a song from a playlist by playlist ID and song ID.
    """
    try:
        playlist = PlayList.objects.get(id=playlist_id)
    except PlayList.DoesNotExist:
        return Response({"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND)

    
    try:
        song_in_playlist = SongsAddedToPlayList.objects.get(PlayListId=playlist, SongID=song_id)
        song_in_playlist.delete()
        return Response({"message": "Song removed successfully from the playlist."}, status=status.HTTP_200_OK)
    
    except SongsAddedToPlayList.DoesNotExist:
        return Response({"error": "Song not found in the specified playlist."}, status=status.HTTP_404_NOT_FOUND)



@api_view(['PUT'])
def UpdatePlaylist(request, playlistId, userId):
    try:
        playlist = PlayList.objects.get(id=playlistId)
    except PlayList.DoesNotExist:
        return Response({"error": "Playlist not found."}, status=status.HTTP_404_NOT_FOUND)

    # Optional: verify user ownership here if you have authentication
    if playlist.UserId.id != userId:
        return Response({"error": "You do not have permission to update this playlist."}, status=status.HTTP_403_FORBIDDEN) 
    

    serializer = PlayListSerializer(playlist, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Playlist updated successfully.", "playlist": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
