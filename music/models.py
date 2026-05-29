# We import the models module from django.db to help us define our database structure.
from django.db import models

# A Model is like a blueprint for a spreadsheet.
# This Genre class tells Django to create a database table for song genres (like Pop, Rock, Jazz).
class Genre(models.Model):
    # A text field that holds the name of the genre.
    # 'max_length=100' sets a limit of 100 characters.
    # 'unique=True' makes sure no two genres can have the exact same name.
    name = models.CharField(max_length=100, unique=True)

    # The __str__ method tells Django how to display this object as plain text.
    # This is extremely helpful when viewing objects in the Django Admin panel!
    def __str__(self):
        # We return the genre's name so it displays as "Pop" instead of "Genre object (1)"
        return self.name


# This Song class defines a database table to hold details about individual tracks.
class Song(models.Model):
    # A text field to hold the song's title (maximum of 255 characters).
    title = models.CharField(max_length=255)
    
    # A text field to store the performing artist's name.
    artist = models.CharField(max_length=255)
    
    # An integer field to store the length of the song in seconds.
    # For example, a 3-minute song will be saved as 180.
    duration = models.IntegerField()

    # Tells Django how to display this song in text form (e.g., inside the Admin panel).
    def __str__(self):
        # We combine the title and the artist to display it beautifully.
        return f"{self.title} by {self.artist}"
