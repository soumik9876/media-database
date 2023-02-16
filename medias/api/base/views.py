from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404

from medias.api.base.serializers import BaseMediaBriefResponseSerializer, BaseMediaSerializer
from medias.api.filters import MediaFilter
from medias.models import Media


class BaseMediaListAPIView(ListAPIView):
    serializer_class = BaseMediaBriefResponseSerializer
    filterset_class = MediaFilter

    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title']

    def get_queryset(self):
        return Media.objects.all()


class BaseMediaRetrieveAPIView(RetrieveAPIView):
    serializer_class = BaseMediaSerializer

    def get_object(self):
        query = self.request.query_params
        return get_object_or_404(Media, id=query.get('id'))


# class BaseUserMediaListCreateAPIView(ListCreateAPIView):
