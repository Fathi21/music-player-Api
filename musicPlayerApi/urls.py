from django.urls import path


from . import views


urlpatterns = [
    path('', views.Api, name='Api'),
    path('Api/MusicList', views.MusicList, name='MusicList'),
]