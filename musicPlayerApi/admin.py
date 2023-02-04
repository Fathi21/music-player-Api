from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(Music)
admin.site.register(Category)
admin.site.register(Liked)
admin.site.register(PlayList)
admin.site.register(SongsAddedToPlayList)

