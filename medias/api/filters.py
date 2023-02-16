from django_filters import rest_framework as filters

from medias.models import Media


class MediaFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    initial_release_gte = filters.DateFilter(field_name='initial_release', lookup_expr='gte')

    class Meta:
        model = Media
        fields = ['language', 'initial_release']
