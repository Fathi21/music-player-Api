from rest_framework.test import APITestCase
from rest_framework import status
from .models import PlayList
from .serializers import PlayListSerializer
from django.contrib.auth.models import User

class GetPlayListTestCase(APITestCase):
    def setUp(self):
        user, _ = User.objects.get_or_create(id=55, defaults={'username': 'myuser'})

        self.playlist1 = PlayList.objects.create(
            PlayListName="My Playlist 1",
            Description="This is my first playlist",
            PhotoCover= "/media/uploads/PhotoCover/pexels-rahul-shah-2268487.jpg",
            CreatedAt = "2023-01-29T00:00:00Z",
            UserId= User.objects.get(id=55)
        )
        self.playlist2 = PlayList.objects.create(
            PlayListName="My Playlist 2",
            Description="This is my second playlist",
            PhotoCover= "/media/uploads/PhotoCover/pexels-rahul-shah-2268487.jpg",
            CreatedAt = "2023-01-29T00:00:00Z",
            UserId= User.objects.get(id=55)
        )

    def test_get_all_playlists(self):
        url = '/Api/GetPlayList'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = PlayListSerializer([self.playlist1, self.playlist2], many=True).data
        self.assertEqual(response.data, expected_data)


