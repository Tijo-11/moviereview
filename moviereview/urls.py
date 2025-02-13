from django.contrib import admin  # Import the Django admin module
from django.urls import path, include  # Import path for URL mapping and include for app-level URLs
from django.conf.urls.static import static  # Import static function for handling media files
from django.conf import settings  # Import settings to access MEDIA_URL and MEDIA_ROOT
from movie.views import index

urlpatterns = [
    path("admin/", admin.site.urls),  # URL route for the Django admin panel

    path('newsapp/', include('newsapp.urls')),  # Includes the URLs of the 'newsapp' app, accessible at /newsapp/
    path('movie/', include('movie.urls')),# Includes the URLs of the 'movie' app, accessible at /movie
    path('accounts/', include('accounts.urls')),
    path('',include('django.contrib.auth.urls')),
    path("", index, name="index"),
]

# Serves media files during development (only needed if MEDIA_URL and MEDIA_ROOT are set in settings.py)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

