from django.urls import path  # Import the path function to define URL patterns
from .import views  # Import views from the current app

urlpatterns = [
    path("", views.home, name="home"),  # Home page
    path("about/", views.about),  # About page (does not have a name assigned)
    path("signup/", views.signup, name="signup"),  # Signup page for new users
    path("<int:movie_id>", views.details, name="detail"),  # Movie details page (expects a movie ID)
    path("<int:movie_id>/create", views.createreview, name="createreview"),  # Create a review for a specific movie
    path('review/<int:review_id>', views.updatereview, name='updatereview'),
    path('review/<int:review_id>/delete',views.deletereview,name='deletereview')
]
