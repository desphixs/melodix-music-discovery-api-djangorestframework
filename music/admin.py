# We import the admin module from django.contrib to handle registers.
from django.contrib import admin
# We import our newly created Genre and Song models from the models.py file in our same directory.
from .models import Genre, Song

# We register the Genre model so it appears as a manageable section in the Django Admin interface.
admin.site.register(Genre)

# We register the Song model so admins can view, add, update, and delete songs in the browser dashboard.
admin.site.register(Song)
