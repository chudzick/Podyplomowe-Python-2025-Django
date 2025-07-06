from django.contrib import admin
from .models import Movie


class MovieAdmin(admin.ModelAdmin):
    list_filter = ('statistics__vote_count',)
    list_display = ('title', 'release_date', 'vote_count', 'vote_average')
    date_hierarchy = 'release_date'

    def vote_count(self, m: Movie):
        return m.statistics.vote_count

    def vote_average(self, m: Movie):
        return m.statistics.vote_average


# Register your models here.
admin.site.register(Movie, MovieAdmin)
