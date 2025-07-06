from django import forms
from django.core.validators import RegexValidator, MinLengthValidator, MinValueValidator
from .models import PopularityRangeValidator, validate_even


class MovieForm(forms.Form):
    # <input type='text'>
    tmdb_id = forms.CharField(
        max_length=255,
        label='TMDB ID',
        validators=[RegexValidator(regex=r'tt\d{7}', message='Proszę podać poprawny TMDB ID!')],
        widget=forms.TextInput(attrs={'placeholder': 'TMDB ID'})
    )
    title = forms.CharField(
        max_length=1000,
        label='Tytuł',
        widget=forms.TextInput(attrs={'placeholder': 'Tytuł'})
    )
    overview = forms.CharField(
        label='Opis',
        validators=[MinLengthValidator(10)],
        widget=forms.Textarea(attrs={'placeholder': 'Opis'})
    )
    # <input type="date"
    release_date = forms.DateField(
        label='Data wydania',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    cast = forms.CharField(
        max_length=1000,
        label='Obsada',
        widget=forms.TextInput(attrs={'placeholder': 'Obsada'})
    )
    genres = forms.CharField(
        max_length=1000,
        label='Gatunki',
        widget=forms.TextInput(attrs={'placeholder': 'Gatunki'})
    )
    director = forms.CharField(
        max_length=1000,
        label='Reżyser',
        widget=forms.TextInput(attrs={'placeholder': 'Reżyser'})
    )
    keyword = forms.CharField(
        label='Słowa kluczowe',
        validators=[MinLengthValidator(10)],
        widget=forms.Textarea(attrs={'placeholder': 'Słowa kluczowe'})
    )

    # Movie Statistics data
    popularity = forms.DecimalField(
        label='Popularność',
        max_digits=20,
        decimal_places=10,
        validators=[PopularityRangeValidator(0, 100), validate_even],
        widget=forms.NumberInput(attrs={'placeholder': '0.0'})
    )
    vote_average = forms.DecimalField(
        label='Średnia głosów',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'placeholder': '0.0'})
    )
    vote_count = forms.IntegerField(
        label='Liczba głosów',
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={'placeholder': '0'})
    )
