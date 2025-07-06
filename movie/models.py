from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, RegexValidator, \
    BaseValidator


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError(f'{value} nie jest wartością parzystą!')


class PopularityRangeValidator(BaseValidator):

    def __init__(self, min, max):
        self.min = min
        self.max = max
        super().__init__(None)

    def __call__(self, value):
        if value < self.min or value > self.max:
            raise ValidationError(f'Zakres popularności musi wynosić od {self.min} do {self.max}')


class MovieStatistics(models.Model):
    popularity = models.DecimalField(max_digits=20, decimal_places=10,
                                     validators=[PopularityRangeValidator(0, 100), validate_even])
    vote_average = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    vote_count = models.IntegerField(validators=[MinValueValidator(0)])

    def vote_average_percent(self):
        return int(self.vote_average * 10)


class Movie(models.Model):
    tmdb_id = models.CharField(max_length=255, validators=[
        RegexValidator(regex=r'tt\d{7}', message='Proszę podać poprawny TMDB ID!')
    ])
    title = models.CharField(max_length=1000)
    overview = models.TextField(validators=[MinLengthValidator(10)])
    release_date = models.DateField()
    cast = models.CharField(max_length=1000)
    genres = models.CharField(max_length=1000)
    director = models.CharField(max_length=1000)
    keyword = models.TextField(validators=[MinLengthValidator(10)])
    statistics = models.OneToOneField(MovieStatistics, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
