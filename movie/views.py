from django.shortcuts import render
from .models import Movie
from django.db.models import Avg, Min, Max, Count
from django.urls import reverse


class Breadcrumb:
    def __init__(self, path, label):
        self.path = path
        self.label = label


# Create your views here.
def all_movies(request):
    found_movies = Movie.objects.all()
    found_movies_aggregation = found_movies.aggregate(
        Count('id'),
        Avg('vote_average'),
        Min('vote_count'),
        Max('vote_count')
    )
    return render(request, 'movie/movie_all.html', {
        'movies': found_movies,
        'details': found_movies_aggregation
    })


def detail_movie(request, tmdb_id):
    found_movie = Movie.objects.get(tmdb_id=tmdb_id)
    return render(request, 'movie/movie_details.html', {
        'movie': found_movie,
        'breadcrumbs': [
            Breadcrumb(reverse('all_movies_url'), 'Wszystkie filmy'),
            Breadcrumb(reverse('detail_movie_url', args=[found_movie.tmdb_id]), found_movie.title),
        ]
    })
