# We import path from django.urls to map our custom paths to the view logic.
from django.urls import path
# We import our class-based views from the views.py file in our same folder.
from .views import GenreListAPIView, SongListAPIView, PlaylistListAPIView

# The urlpatterns list holds all of the specific URL routes for the music app.
urlpatterns = [
    # Route for listing and creating genres.
    # We call '.as_view()' on class-based views to transform the class into a callable function that Django's router can execute.
    path('genres/', GenreListAPIView.as_view(), name='genre-list'),
    
    # Route for listing and creating songs.
    path('songs/', SongListAPIView.as_view(), name='song-list'),
    
    # Route for listing and creating playlists.
    path('playlists/', PlaylistListAPIView.as_view(), name='playlist-list'),
]
