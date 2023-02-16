from django.urls import path

from medias.api.v1.views import MediaListCreateAPIView, MediaRetrieveAPIView, UserMediaListCreateAPIView

urlpatterns = [
    path('media/', MediaListCreateAPIView.as_view(), name='media'),
    path('media/item/', MediaRetrieveAPIView.as_view(), name='media-item'),
    path('user-media/', UserMediaListCreateAPIView.as_view(), name='user-media')
]
