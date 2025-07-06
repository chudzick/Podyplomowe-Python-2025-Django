from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_movies, name='all_movies_url'),
    path('collections', views.all_collections, name='all_collections_url'),
    path('collections/<int:id>', views.detail_collection, name='detail_collection_url'),
    path('add', views.add_movie, name='add_movie_url'),
    path('<tmdb_id>', views.detail_movie, name='detail_movie_url'),
]
