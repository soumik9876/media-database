import csv
import datetime
import gzip
import os
import shutil

import requests
import wget

from media_database.settings import BASE_DIR, OMDB_ROOT, OMDB_API_KEY
from medias.models import Media, Genre


class ImdbDataClient:
    title_rating_file = 'data_files/title.ratings.tsv'
    title_rating_file_url = 'https://datasets.imdbws.com/title.ratings.tsv.gz'

    def download_and_extract_title_rating(self, name, tsv_path):
        gzip_path = f'{BASE_DIR}/{name}.gz'
        wget.download(self.title_rating_file_url, gzip_path)
        print('Downloaded gzip file')
        with gzip.open(gzip_path, 'rb') as f_in, open(tsv_path, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
            f_in.close()
            f_out.close()
            print('Extracted file')
        os.remove(gzip_path)
        print('Removed gzip file')

    def read_tsv(self, name):
        tsv_path = f'{BASE_DIR}/{name}'
        if os.path.exists(tsv_path) is False:
            self.download_and_extract_title_rating(name, tsv_path)

        with open(tsv_path) as file:
            tsv_file = list(csv.reader(file, delimiter='\t'))
            # print(tsv_file[:4])
            file.close()
        return tsv_file

    def get_sort_key(self, k):
        try:
            return int(k)
        except:
            return 0

    def get_top_rated_medias(self):
        medias = sorted(self.read_tsv(self.title_rating_file), key=lambda t: self.get_sort_key(t[2]), reverse=True)
        medias.pop(0)
        cnt = 0
        for media in medias:
            try:
                if not Media.objects.filter(imdb_id=media[0]).exists():
                    new_media = self.create_media(media[0])
                    print(new_media)
                    cnt += 1
            except Exception as e:
                print(f'Media create error -> {e} | imdb_id -> {media[0]}')

            if cnt >= 1000:
                break

    def get_media_details_from_omdb(self, imdb_id):
        response = requests.get(f'{OMDB_ROOT}?apiKey={OMDB_API_KEY}&i={imdb_id}&plot=full').json()
        return response

    def create_media(self, media_id):
        response = self.get_media_details_from_omdb(imdb_id=media_id)
        title = response.get('Title', '')
        year = response.get('Year', '').split('–')
        try:
            initial_release = int(year[0])
        except:
            initial_release = None

        try:
            final_release = int(year[1])
        except:
            final_release = None
        runtime = response.get('Runtime', '')
        genres = response.get('Genre', '').split(',')
        director = response.get('Director', '')
        writer = response.get('Writer', '')
        actors = response.get('Actors', '')
        plot = response.get('Plot', '')
        language = response.get('Language', '')
        region = response.get('Country', '')
        awards = response.get('Awards', '')
        box_office = response.get('Box Office', '')
        banner = response.get('Poster', '')

        imdb_rating = response.get('imdbRating', '')
        try:
            imdb_rating = float(imdb_rating)
        except:
            imdb_rating = 'N/A'

        meta_score = response.get('Metascore', '')
        try:
            meta_score = float(meta_score)
        except:
            meta_score = 'N/A'

        try:
            rotten_tomato = next(
                filter(lambda x: x.get('Source', '') == 'Rotten Tomatoes', response.get('Ratings'))).get(
                'Value')
        except:
            rotten_tomato = 'N/A'

        media_type = response.get('Type', '')
        imdb_id = response.get('imdbID', '')

        try:
            media = Media.objects.create(
                title=title,
                initial_release=initial_release,
                final_release=final_release,
                runtime=runtime,
                type=media_type,
                awards=awards,
                box_office=box_office,
                director=director,
                writers=writer,
                cast=actors,
                plot=plot,
                language=language,
                region=region,
                banner=banner,
                ratings={
                    'imdb': imdb_rating,
                    'metacritic': meta_score,
                    'rotten_tomato': rotten_tomato
                },
                imdb_id=imdb_id
            )
        except Exception as e:
            print(f'Media object create error --> {e}')
            raise e

        for genre in genres:
            obj = Genre.objects.get_or_create(title=genre.strip())[0]
            obj.medias.add(media)

        return media
