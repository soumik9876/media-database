from django.db import models
from django.utils.translation import gettext_lazy as _
from core.models import BaseModel


# Create your models here.
class Media(BaseModel):
    title = models.CharField(max_length=200, verbose_name=_('Media'))
    plot = models.TextField(verbose_name=_('Synopsis'), blank=True)
    language = models.CharField(max_length=30, verbose_name=_('Language'), blank=True)
    region = models.CharField(max_length=30, verbose_name=_('Region'), blank=True)
    runtime = models.CharField(max_length=30, verbose_name=_('Runtime'), blank=True)

    director = models.CharField(max_length=100, verbose_name=_('Director'), blank=True)
    writers = models.TextField(verbose_name=_('Writers'), blank=True)
    cast = models.TextField(verbose_name=_('Cast'), blank=True)

    banner = models.URLField(max_length=255, verbose_name=_('Banner'), blank=True)
    trailer_link = models.URLField(verbose_name=_('Trailer link'), blank=True)
    # Dates
    initial_release = models.DateTimeField(verbose_name=_('Initial release date'), blank=True, null=True)
    final_release = models.DateTimeField(verbose_name=_('Final release date'), blank=True, null=True)

    ratings = models.JSONField(verbose_name=_('Ratings'), blank=True)
    imdb_id = models.CharField(max_length=30, verbose_name=_('Imdb ID'), blank=True)

    extra = models.JSONField(verbose_name=_('Extra'), default=dict, blank=True)

    class Meta:
        verbose_name = _('Media')
        verbose_name_plural = _('Medias')

    def __str__(self):
        return self.title


class Genre(BaseModel):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    movies = models.ManyToManyField(to=Media, verbose_name=_('Movies'))

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.title
