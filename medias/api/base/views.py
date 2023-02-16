from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404

from medias.api.base.serializers import BaseMediaBriefResponseSerializer, BaseMediaSerializer, BaseUserMediaSerializer
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


class BaseUserMediaListCreateAPIView(ListCreateAPIView):
    serializer_class = BaseUserMediaSerializer

    def get_queryset(self):
        return self.request.user.usermedia_set.all()
