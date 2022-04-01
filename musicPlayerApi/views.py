from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *


def Api(request):

    return JsonResponse({"Name" : "Fathi"})


@api_view(['GET'])
def MusicList(request):

    try:
        Musics = Music.objects.all()
    except Musics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(Musics)
    if request.method == 'GET':
        serializer = MusicSerializer(Musics, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def SongSelected(request, pk):

    try:
        Musics = Music.objects.filter(id=pk)
    except Musics.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MusicSerializer(Musics, many=True)
        return Response(serializer.data)
