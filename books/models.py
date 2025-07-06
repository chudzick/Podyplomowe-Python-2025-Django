from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_date = models.DateField()
    vote_average = models.DecimalField(max_digits=5, decimal_places=2)
    vote_count = models.IntegerField()
    description = models.TextField(default='N/A')

    def __str__(self):
        return f'{self.title}'

