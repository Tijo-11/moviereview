from django.urls import path  # Import path to define URL patterns
from . import views  # Import views.py from the current directory

# Define URL patterns for this app
urlpatterns = [
    path('', views.news, name='news'),  # Maps the base URL ('') of this app to the 'news' view
    # The empty string ('') means this is the default route when accessing this app.
    # The 'name' parameter allows referencing this URL in templates and redirects.
]
