from django.shortcuts import render, get_object_or_404
from .models import Movie, MovieCollection
from django.db.models import Avg, Min, Max, Count
from django.urls import reverse


class Breadcrumb:
    def __init__(self, path, label):
        self.path = path
        self.label = label


# Create your views here.
def all_movies(request):
    found_movies = Movie.objects.select_related('statistics').all()
    found_movies_aggregation = found_movies.aggregate(
        Count('id'),
        Avg('statistics__vote_average'),
        Min('statistics__vote_count'),
        Max('statistics__vote_count')
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


def all_collections(request):
    movie_collections = MovieCollection.objects.all().annotate(movie_count=Count('movies'))
    return render(request, 'collection/collection_all.html', {
        'collections': movie_collections,
    })


def detail_collection(request, id):
    movie_collection = get_object_or_404(MovieCollection, id=id)
    return render(request, 'collection/collection_details.html', context={
        'collection': movie_collection,
        'breadcrumbs': [
            Breadcrumb(reverse('all_collections_url'), 'Wszystkie kolekcje'),
            Breadcrumb(reverse('detail_collection_url', args=[movie_collection.id]), movie_collection.name),
        ]
    })
