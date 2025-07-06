import datetime

from django.db import migrations
import csv
from movie.models import Movie, MovieStatistics
from django.db import transaction


def load_movies(apps, schema_editor):
    with open('movie/migrations/movies.csv', 'r', encoding='utf-8') as movies:
        reader = csv.DictReader(movies, delimiter=',')

        for row in reader:
            stats = MovieStatistics.objects.create(
                popularity=row['popularity'],
                vote_average=row['vote_average'],
                vote_count=row['vote_count'],
            )

            Movie.objects.create(
                tmdb_id=row['tmdb_id'],
                title=row['original_title'],
                overview=row['overview'],
                release_date=datetime.datetime.strptime(row['release_date'], '%m/%d/%Y'),
                cast=row['cast'],
                genres=row['genres'],
                director=row['director'],
                keyword=row['keywords'],
                statistics=stats
            )


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(load_movies)
    ]
