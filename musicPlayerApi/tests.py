from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PlayList
from .serializers import PlayListSerializer
from .views import GetPlayListById


class GetPlayListByIdTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create a test playlist
        self.playlist = PlayList.objects.create(
            PlayListName='Test Playlist',
            Description='Test Description',
            PhotoCover=None,
            UserId=self.user,
            CreatedAt=timezone.now()
        )

    def test_get_playlist_by_id(self):
        request = self.factory.get(
            f'/Api/GetPlayListById/{self.playlist.pk}/')
        view = GetPlayListById
        response = view(request, pk=self.playlist.pk)

        self.assertEqual(response.status_code, 200)

        serializer = PlayListSerializer(self.playlist)
        self.assertEqual(response.data, serializer.data)

    def test_get_nonexistent_playlist(self):
        request = self.factory.get('/Api/GetPlayListById/999/')
        view = GetPlayListById
        response = view(request, pk=999)

        self.assertEqual(response.status_code, 404)
