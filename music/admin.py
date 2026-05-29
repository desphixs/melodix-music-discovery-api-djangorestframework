# We import the admin module from django.contrib to handle registers.
from django.contrib import admin
# We import our Genre, Song, and Playlist models from the models.py file.
from .models import Genre, Song, Playlist

# We register the Genre model so it appears as a manageable section in the Django Admin interface.
admin.site.register(Genre)

# We register the Song model so admins can view, add, update, and delete songs in the browser dashboard.
admin.site.register(Song)

# We register the Playlist model so admins can manage playlists and see Many-to-Many associations in the admin panel.
admin.site.register(Playlist)
