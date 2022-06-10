from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


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
    CategoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.Title) if self.Title else ''
    
    class Meta:
        verbose_name_plural = "Music"


class Favourite(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    MusicId = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.MusicId) if self.MusicId else ''
    
    class Meta:
        verbose_name_plural = "Favourite"


class Liked(models.Model):
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    MusicId = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.MusicId) if self.MusicId else ''
    
    class Meta:
        verbose_name_plural = "Liked"


class Album(models.Model):
    AlbumName = models.TextField(blank=False, null=False)
    UserId = models.ForeignKey(User, on_delete=models.CASCADE)
    MusicId = models.ForeignKey(Music, on_delete=models.CASCADE)
    CreatedAt = models.DateField(default=timezone.now)


    def __str__(self):
        return str(self.MusicId) if self.MusicId else ''
    
    class Meta:
        verbose_name_plural = "Album"