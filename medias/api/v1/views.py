from medias.api.base.views import BaseMediaListAPIView, BaseMediaRetrieveAPIView, BaseUserMediaListCreateAPIView
from medias.api.v1.serializers import MediaSerializer, MediaBriefResponseSerializer, UserMediaSerializer


class MediaListCreateAPIView(BaseMediaListAPIView):
    serializer_class = MediaBriefResponseSerializer


class MediaRetrieveAPIView(BaseMediaRetrieveAPIView):
    serializer_class = MediaSerializer


class UserMediaListCreateAPIView(BaseUserMediaListCreateAPIView):
    serializer_class = UserMediaSerializer
