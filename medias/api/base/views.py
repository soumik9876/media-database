from django.db.models import Q
from rest_framework.decorators import permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView, get_object_or_404, UpdateAPIView, \
    RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core.api.paginations import StandardResultsSetPagination
from core.api.permissions import IsObjectOwner
from medias.api.base.serializers import BaseMediaBriefResponseSerializer, BaseMediaSerializer, BaseUserMediaSerializer
from medias.api.filters import MediaFilter
from medias.models import Media, UserMedia


class BaseMediaListAPIView(ListAPIView):
    serializer_class = BaseMediaBriefResponseSerializer
    filterset_class = MediaFilter
    pagination_class = StandardResultsSetPagination

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.usermedia_set.all()


class BaseUserMediaRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    """
        Pass the media_id or id of usermedia in data to update the user media
    """
    serializer_class = BaseUserMediaSerializer
    permission_classes = [IsAuthenticated, IsObjectOwner]

    def get_object(self):
        query = self.request.data
        media_id, user_media_id = query.get('media', None), query.get('id', None)
        q_exp = Q(id=user_media_id) if user_media_id is not None else Q(media_id=media_id, user=self.request.user)
        return UserMedia.objects.filter(q_exp).first()
