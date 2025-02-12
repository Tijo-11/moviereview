from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=100)
    producer=models.CharField(max_length=100, blank=True)
    synopsis=models.TextField(blank=True)
    tagline=models.TextField()
    director=models.CharField(max_length=100)
    writers=models.CharField(max_length=100)
    editor=models.CharField(max_length=100)
    music=models.CharField(max_length=100)
    cinematography=models.CharField(max_length=100)
    keycast=models.CharField(max_length=1000)
    
    image=models.ImageField(upload_to='movie/images/')
class Review(models.Model):
    STAR_CHOICES = [(i, str(i)) for i in range(1, 11)] # Choices from 1 to 10
    text=models.CharField(max_length=2000)
    rating = models.IntegerField(choices=STAR_CHOICES)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    watchAgain =models.BooleanField(default=False)

    
    
    
    def __str__(self):
        return f"{self.user.username}- {self.movie.title} ({self.rating}★)\n{self.text}"
#model for requested movies

class MovieRequest(models.Model):
    movie_name = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)  # Stores request time
    remarks = models.TextField(blank=True, null=True)  # Optional remarks field for admin
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie_name', 'year'], name='unique_movie_request')
        ]

    def __str__(self):
        return f"{self.movie_name} ({self.year})"

