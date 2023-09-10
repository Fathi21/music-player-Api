from django.urls import path
from . import views


urlpatterns = [
    path('Api/GetAllMusic', views.GetAllMusic, name='GetAllMusic'),
    path('Api/GetSongById/<int:pk>', views.GetSongById, name='GetSongById'),
    path('Api/GetLikesBySongId/<int:pk>', views.GetLikesBySongId, name='GetLikesBySongId'),
    path('Api/LikeASongById', views.LikeASongById, name='LikeASongById'),
    path('Api/GetAllLikedSongs', views.GetAllLikedSongs, name='GetAllLikedSongs'),
    path('Api/GetAllLikedSongsByUser/<int:pk>', views.GetAllLikedSongsByUser, name='GetAllLikedSongsByUser'),
    path('Api/GetUserById/<int:pk>', views.GetUserById, name='GetUserById'),
    path('Api/UserByUserName/<str:username>', views.UserByUserName, name='UserByUserName'),
    path('Api/ExistUsers', views.ExistUsers, name='ExistUsers'),
    path('Api/Register', views.Register, name='Register'),
    path('Api/login/<str:username>/<str:password>', views.login, name='login'),
    path('Api/GetPlayList', views.GetPlayList, name='GetPlayList'),
    path('Api/GetPlayListById/<int:pk>', views.GetPlayListById, name='GetPlayListById'),
    path('Api/GetSongsAddedToPlayListById/<int:pk>', views.GetSongsAddedToPlayListById, name='GetSongsAddedToPlayListById'),
    path('Api/GetSongfromPlaylist/<int:pk>', views.GetSongfromPlaylist, name='GetSongfromPlaylist'),
    path('Api/CreateNewPlayList', views.CreateNewPlayList, name='CreateNewPlayList'),
    path('Api/GetCategoryById/<int:pk>', views.GetCategoryById, name='GetCategoryById'),
    path('Api/AddSongSongToThePlayList', views.AddSongSongToThePlayList, name='AddSongSongToThePlayList'),

]