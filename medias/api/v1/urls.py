from django.urls import path

from medias.api.v1.views import MediaListCreateAPIView, MediaRetrieveAPIView

urlpatterns = [
    path('media/', MediaListCreateAPIView.as_view(), name='media'),
    path('media/item/', MediaRetrieveAPIView.as_view(), name='media-item'),
]
