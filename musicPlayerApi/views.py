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

    if request.method == 'GET':
        Musics = Music.objects.all()
        serializer = MusicSerializer(({"Name" : "Fathi"}), many=True)
        return Response(serializer.data)