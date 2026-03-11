"""URL configuration for the project."""

from django.urls import include, path

urlpatterns = [
    path('', include('apps.health.urls')),
    path('', include('apps.users.urls')),
    path('', include('apps.events.urls')),
]
