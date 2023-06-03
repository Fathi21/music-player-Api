from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
from django.db import models

class Category(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.TextField(blank=False, null=False)
    Description = models.TextField(blank=False, null=False)
    CreatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.Title) if self.Title else ''
    
    class Meta:
        verbose_name_plural = "Category"


class Music(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Artist = models.TextField(blank=False, null=False)
    Title = models.TextField(blank=False, null=False)
    MusicFile = models.FileField(upload_to ='uploads/MusicFile')
    PhotoCover = models.ImageField(upload_to ='uploads/PhotoCover')
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.Title) if self.Title else ''
    
    class Meta:
        verbose_name_plural = "Music"


class Liked(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    SongID = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.UserId} > {self.SongID}' if self.UserId and self.SongID else ''
    
    class Meta:
        verbose_name_plural = "Liked"


class PlayList(models.Model):
    PlayListName = models.TextField(blank=False, null=False)
    Description = models.TextField(blank=False, null=False)
    PhotoCover = models.ImageField(blank=True, null=True, upload_to ='uploads/PhotoCover')
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return str(self.PlayListName) if self.PlayListName else ''
    
    class Meta:
        verbose_name_plural = "PlayList"


class SongsAddedToPlayList(models.Model):
    PlayListId = models.ForeignKey(PlayList, on_delete=models.CASCADE)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    SongID = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.PlayListId} > {self.SongID}' if self.PlayListId and self.SongID else ''
    
    class Meta:
        verbose_name_plural = "songs in playlist"


