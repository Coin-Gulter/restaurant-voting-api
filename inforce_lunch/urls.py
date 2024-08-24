# General urls
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site URL
    path('authentication/', include('authentication.urls')),  # URLs for authentication app
    path('restaurants/', include('restaurants.urls')),  # URLs for restaurant management app
    path('voting/', include('voting.urls')),  # URLs for voting functionality
]
