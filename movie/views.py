from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Movie, Review, MovieRequest
from .forms import ReviewForm, MovieRequestForm

from django.views.decorators.cache import cache_control  # For caching control
from django.views.decorators.cache import never_cache


# Create your views here.
def home(request):
    searchTerm = request.GET.get('searchMovie')
    message = ""
    form = MovieRequestForm()

    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    if request.method == "POST":
        form = MovieRequestForm(request.POST)
        if form.is_valid():
            movie_name = form.cleaned_data["movie_name"]
            year = form.cleaned_data["year"]

            # ✅ Fix: Ensure the filter query works correctly
            if MovieRequest.objects.filter(movie_name__iexact=movie_name, year=year).exists():
                message = "Movie already requested!"
            else:
                form.save()
                message = "Movie request submitted successfully!"

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies,
        'form': form,
        'message': message
    })


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email':email})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Prevents caching of the page
def details(request, movie_id):
    movie= get_object_or_404(Movie, pk=movie_id)
    reviews=Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie':movie,'reviews':reviews})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Prevents caching of the page
def createreview(request, movie_id):
    # Get the movie object by ID or return a 404 error if not found
    movie = get_object_or_404(Movie, pk=movie_id)

    # If the request method is GET, render the review creation form
    if request.method == 'GET':
        return render(request, 'createreview.html', {'form': ReviewForm(), 'movie': movie})

    else:
        try:
            # Bind form data from POST request
            form = ReviewForm(request.POST)

            # Save the form without committing to database yet
            newReview = form.save(commit=False)

            # Assign user and movie to the review
            newReview.user = request.user
            newReview.movie = movie

            # Save the review to the database
            newReview.save()

            # Redirect to the movie detail page after successful review submission
            return redirect('detail', newReview.movie.id)

        except ValueError:
            # If invalid data is submitted, re-render the form with an error message
            return render(request, 'createreview.html', {
                'form': ReviewForm(),
                'error': 'Invalid data submitted, please try again.'
            })


@cache_control(no_cache=True, must_revalidate=True, no_store=True)  # Prevents caching of the page
def updatereview(request, review_id):
    # Fetch the review based on review_id, ensuring it belongs to the logged-in user
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    if request.method == 'GET':
        # Pre-fill the form with the existing review data
        form = ReviewForm(instance=review)
        return render(request, 'updatereview.html', {'review': review, 'form': form})
    
    else:
        try:
            # Update the review with new data from the submitted form
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('detail', review.movie.id)  # Redirect to movie details page after updating
        
        except ValueError:
            # Handle invalid form input and re-render the update page with an error message
            return render(request, 'updatereview.html', {'review': review, 'form': form, 'error': 'Bad data in form'})
        

from django.shortcuts import get_object_or_404, redirect
from .models import Review

def deletereview(request, review_id):
    # Fetch the review, ensuring it belongs to the logged-in user
    review = get_object_or_404(Review, pk=review_id, user=request.user)
    
    # Delete the review from the database
    review.delete()
    
    # Redirect to the movie details page after successful deletion
    return redirect('detail', review.movie.id)

def about(request):
    return HttpResponse("Hi Welcome to About Page!")
