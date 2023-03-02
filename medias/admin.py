from django.contrib import admin
from django.contrib.admin import display

from .models import *


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'initial_release', 'ratings', 'genres']
    search_fields = ['title']
    list_filter = ['type']

    @display(description='Genre')
    def genres(self, obj: Media):
        return ','.join(list(obj.genre_set.values_list('title', flat=True)))


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title', 'media_count']

    @display(description='Media count')
    def media_count(self, obj: Genre):
        return obj.medias.count()


@admin.register(UserMedia)
class UserMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'media']
    search_fields = ['user__username', 'user__email']
