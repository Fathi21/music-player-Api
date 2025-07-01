from django.urls import path

from . import views


urlpatterns = [
    path('', views.Api, name='Api'),
    path('Api/GetAllMusic', views.GetAllMusic, name='GetAllMusic'),
    path('Api/GetSongById/<int:pk>', views.GetSongById, name='GetSongById'),
    path('Api/GetLikesBySongId/<int:pk>', views.GetLikesBySongId, name='GetLikesBySongId'),
    path('Api/LikeASongById', views.LikeASongById, name='LikeASongById'),
    path('Api/GetAllLikedSongs', views.GetAllLikedSongs, name='GetAllLikedSongs'),
    path('Api/GetAllLikedSongsByUser/<int:user_id>', views.GetAllLikedSongsByUser, name='GetAllLikedSongsByUser'),
    path('Api/UserById/<int:pk>', views.UserById, name='UserById'),
    path('Api/UserByUserName/<str:username>', views.UserByUserName, name='UserByUserName'),
    path('Api/ExistUsers', views.ExistUsers, name='ExistUsers'),
    path('Api/Register', views.Register, name='Register'),
    path('Api/login/<str:username>/<str:password>', views.login, name='login'),
    path('Api/GetPlayList', views.GetPlayList, name='GetPlayList'),
    path('Api/GetPlayListById/<int:pk>', views.GetPlayListById, name='GetPlayListById'),
    path('Api/GetSongsAddedToPlayList', views.GetSongsAddedToPlayList, name='GetSongsAddedToPlayList'),
    path('Api/CreateNewPlayListAddSong', views.CreateNewPlayListAddSong, name='CreateNewPlayListAddSong'),
    path ('Api/GetSongsInPlaylistById/<int:pk>', views.GetSongsInPlaylistById, name='GetSongsInPlaylistById'),
    path('Api/RemoveSongFromPlaylist/<int:playlist_id>/<int:song_id>', views.RemoveSongFromPlaylist, name='RemoveSongFromPlaylist'),
    path('Api/UpdatePlaylist/<int:playlistId>/<int:userId>', views.UpdatePlaylist, name='UpdatePlaylist'),
    path('Api/DeletePlayList/<int:playlist_id>', views.DeletePlayList, name='DeletePlayList'),

]