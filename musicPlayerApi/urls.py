from django.urls import path


from . import views


urlpatterns = [
    path('', views.Api, name='Api'),
    path('Api/GetAllMusic', views.GetAllMusic, name='GetAllMusic'),
    path('Api/GetSongById/<int:pk>', views.GetSongById, name='GetSongById'),
    path('Api/GetLikesBySongId/<int:pk>', views.GetLikesBySongId, name='GetLikesBySongId'),
    path('Api/LikeASongById/<int:pk>', views.LikeASongById, name='LikeASongById'),

]