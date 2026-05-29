# We import the admin module from django.contrib to handle registers.
from django.contrib import admin
# We import our Genre, Song, Playlist, and Comment models from the models.py file.
from .models import Genre, Song, Playlist, Comment

# We register the Genre model so it appears as a manageable section in the Django Admin interface.
admin.site.register(Genre)

# We register the Song model so admins can view, add, update, and delete songs in the browser dashboard.
admin.site.register(Song)

# We register the Playlist model so admins can manage playlists and see Many-to-Many associations in the admin panel.
admin.site.register(Playlist)

# We register the Comment model so admins can moderate and view comment threads inside the dashboard.
admin.site.register(Comment)
