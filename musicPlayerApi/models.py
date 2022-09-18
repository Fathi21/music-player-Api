from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
from colorfield.fields import ColorField
from django.db import models

class Category(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.TextField(blank=False, null=False)
    Description = models.TextField(blank=False, null=False)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.Title) if self.Title else ''
    
    class Meta:
        verbose_name_plural = "Category"


class Music(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    Title = models.TextField(blank=False, null=False)
    MusicFile = models.FileField(upload_to ='uploads/MusicFile')
    PhotoCover = models.ImageField(upload_to ='uploads/PhotoCover')
    color = ColorField(default='#76b96a')
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.Title) if self.Title else ''
    
    class Meta:
        verbose_name_plural = "Music"


class Liked(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    SongID = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.SongID) if self.SongID else ''
    
    class Meta:
        verbose_name_plural = "Liked"


class PlayList(models.Model):
    PlayListName = models.TextField(blank=False, null=False)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    SongID = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)


    def __str__(self):
        return str(self.SongID) if self.SongID else ''
    
    class Meta:
        verbose_name_plural = "PlayList"


class Comment(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    SongID = models.ForeignKey(Music, on_delete=models.CASCADE)
    body = models.TextField(blank=False, null=False)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.UserId) if self.UserId else ''
    
    class Meta:
        verbose_name_plural = "Comment"

