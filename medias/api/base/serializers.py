from rest_framework import serializers

from medias.models import Media, Genre


class BaseMediaSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()

    class Meta:
        model = Media
        fields = '__all__'

    def get_genre(self, obj: Media):
        genre_list = list(obj.genre_set.all().values_list('title'))
        return ','.join(genre_list)


class BaseMediaBriefResponseSerializer(BaseMediaSerializer):
    class Meta(BaseMediaSerializer.Meta):
        fields = ['id', 'title', 'language', 'runtime', 'banner', 'initial_release', 'ratings']


class BaseGenreSerializer(serializers.ModelSerializer):
    media_count = serializers.SerializerMethodField()

    class Meta:
        model = Genre
        fields = '__all__'

    def get_media_count(self, obj: Genre):
        return obj.medias.count()
