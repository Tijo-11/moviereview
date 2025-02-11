from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField()
    synopsis=models.TextField(blank=True)
    key_details=models.TextField(blank=True)
    image=models.ImageField(upload_to='movie/images/')
    url=models.URLField(blank=True)
class Review(models.Model):
    STAR_CHOICES = [(i, str(i)) for i in range(1, 11)] # Choices from 1 to 10
    text=models.CharField(max_length=2000)
    rating = models.IntegerField(choices=STAR_CHOICES)
    date=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE)
    watchAgain =models.BooleanField(default=False)

    
    
    
    def __str__(self):
        return f"{self.user.username}- {self.movie.title} ({self.rating}★)\n{self.text}"
#model for requested movies

class MovieRequest(models.Model):
    movie_name = models.CharField(max_length=255)
    tags = models.CharField(max_length=255, blank=True, null=True)  # Optional
    language = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    requested_at = models.DateTimeField(auto_now_add=True)  # Stores request time
    
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['movie_name', 'year'], name='unique_movie_request')
        ]

    def __str__(self):
        return f"{self.movie_name} ({self.year})"

