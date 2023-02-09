from django.contrib import admin
from django.contrib.admin import display

from .models import *


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    list_display = ['title', 'type', 'initial_release', 'final_release', 'ratings', 'genre']
    search_fields = ['title']
    list_filter = ['type']

    @display(description='Genre')
    def genres(self, obj: Media):
        return ','.join(list(obj.genre_set.values_list('title')))


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(UserMedia)
class UserMediaAdmin(admin.ModelAdmin):
    list_display = ['user', 'media']
    search_fields = ['user__username', 'user__email']
