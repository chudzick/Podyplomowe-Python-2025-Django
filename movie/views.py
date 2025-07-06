import datetime

from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, MovieCollection, MovieStatistics, User
from django.db.models import Avg, Min, Max, Count
from django.urls import reverse
from .forms import MovieForm, MovieCollectionForm
from django.views import View


class Breadcrumb:
    def __init__(self, path, label):
        self.path = path
        self.label = label


# Create your views here.
def all_movies(request):
    filter = request.GET.get('title')

    if filter and len(filter) >= 3:
        found_movies = Movie.objects.select_related('statistics').filter(title__contains=filter)
    else:
        found_movies = Movie.objects.select_related('statistics').all()

    found_movies_aggregation = found_movies.aggregate(
        Count('id'),
        Avg('statistics__vote_average'),
        Min('statistics__vote_count'),
        Max('statistics__vote_count')
    )
    return render(request, 'movie/movie_all.html', {
        'filter': filter,
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


def add_movie(request):
    if request.method == 'POST':
        stats = MovieStatistics.objects.create(
            popularity=request.POST['popularity'],
            vote_average=request.POST['vote_average'],
            vote_count=request.POST['vote_count'],
        )

        Movie.objects.create(
            tmdb_id=request.POST['tmdb_id'],
            title=request.POST['title'],
            overview=request.POST['overview'],
            release_date=datetime.datetime.strptime(request.POST['release_date'], '%Y-%m-%d'),
            cast=request.POST['cast'],
            genres=request.POST['genres'],
            director=request.POST['director'],
            keyword=request.POST['keywords'],
            statistics=stats
        )
        return redirect('all_movies_url')

    return render(request, 'movie/movie_add.html')


def add_movie_with_form(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            stats = MovieStatistics.objects.create(
                popularity=data['popularity'],
                vote_average=data['vote_average'],
                vote_count=data['vote_count'],
            )

            Movie .objects.create(
                tmdb_id=data['tmdb_id'],
                title=data['title'],
                overview=data['overview'],
                release_date=data['release_date'],
                cast=data['cast'],
                genres=data['genres'],
                director=data['director'],
                keyword=data['keyword'],
                statistics=stats
            )
            return redirect('all_movies_url')
        else:
            print(form.errors)
    else:
        form = MovieForm()

    return render(request, 'movie/movie_add_with_form.html', {
        'form': form
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


class AddCollectionView(View):

    def get(self, request):
        form = MovieCollectionForm()
        return render(request, 'collection/collection_add.html', {
            'form': form
        })

    def post(self, request):
        form = MovieCollectionForm(request.POST)

        if form.is_valid():
            collection = form.save(commit=False)
            collection.owner = User.objects.all()[0]
            collection.save()
            form.save_m2m()

            return redirect('all_collections_url')

        return render(request, 'collection/collection_add.html', {
            'form': form
        })
