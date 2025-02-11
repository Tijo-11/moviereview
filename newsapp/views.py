from django.shortcuts import render  # Import render to render HTML templates
from django.http import HttpResponse  # Import HttpResponse (not used in this function but useful for basic responses)

# Create your views here.
def news(request):  # Defines a view function named 'news' that handles HTTP requests
    return render(request, "news.html")  # Renders the 'news.html' template and returns the response
