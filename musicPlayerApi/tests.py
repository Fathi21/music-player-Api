from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import User
from django.utils import timezone
from .models import PlayList
from rest_framework.test import APIClient
from rest_framework import status
from .serializers import PlayListSerializer
from .views import GetPlayListById
import pdb  # Import the pdb module
from django.urls import reverse


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



class CreateNewPlayListTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.valid_data = {
            "id": 1,
            "PlayListName": "play List 1",
            "Description": "Now that your identity is set up, you can configure the default text editor that will be used when Git needs you to type in a message. If not configured, Git uses your system’s default edito",
            "PhotoCover": "/media/uploads/PhotoCover/pexels-rahul-shah-2268487.jpg",
            "CreatedAt": "2023-01-29T18:20:31Z",
            "UserId": 55
        }
        self.invalid_data = {
            'PlayListName': '',
            'Description': 'Test playlist description',
            'UserId': self.user.id,
        }

 # The above class is a test case for creating a new playlist in a music application, testing both
 # valid and invalid data inputs.
    
class CreateNewPlayListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.valid_data = {'PlayListName': 'New Playlist', 'Description': 'Playlist description', 'UserId': self.user.id}
        self.invalid_data = {'PlayListName': '', 'Description': '', 'UserId': self.user.id}

    def test_create_new_playlist_valid_data(self):
        response = self.client.post(reverse('CreateNewPlayList'), self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PlayList.objects.count(), 1)
        self.assertEqual(PlayList.objects.get().PlayListName, 'New Playlist')

    def test_create_new_playlist_invalid_data(self):
        """
        The function tests the behavior of creating a new playlist with invalid data.
        """
        response = self.client.post(reverse('CreateNewPlayList'), self.invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PlayList.objects.count(), 0)

    def test_create_new_playlist_existing_name(self):
        """
        The function tests if creating a new playlist with an existing name returns a 400 bad request
        status code and does not create a new playlist.
        """
        PlayList.objects.create(PlayListName='Existing Playlist', Description='Existing description', UserId=self.user)
        response = self.client.post(reverse('CreateNewPlayList'), self.valid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(PlayList.objects.count(), 1)  # Existing playlist count should remain 1