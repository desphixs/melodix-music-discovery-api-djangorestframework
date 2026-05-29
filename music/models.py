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


# This Playlist class defines a database table that groups multiple songs together under a specific genre.
class Playlist(models.Model):
    # A text field to hold the playlist's title (e.g., "Chill Sunday Morning").
    title = models.CharField(max_length=255)
    
    # A text field for a longer description explaining the mood or purpose of the playlist.
    description = models.TextField()

    # A ForeignKey represents a "One-to-Many" database relationship.
    # In this case, each playlist is linked to EXACTLY ONE Genre.
    # 'on_delete=models.PROTECT' is a security guard: it prevents deleting a genre if it is currently being used by any playlists.
    # 'related_name="playlists"' allows us to query all playlists associated with a genre by writing genre.playlists.all()
    genre = models.ForeignKey(Genre, on_delete=models.PROTECT, related_name='playlists')

    # A ManyToManyField represents a "Many-to-Many" database relationship.
    # A playlist can contain many songs, and the same song can belong to many different playlists.
    # 'related_name="playlists"' lets us query all playlists a song belongs to by writing song.playlists.all()
    songs = models.ManyToManyField(Song, related_name='playlists')

    # Tells Django how to display this playlist in text format.
    def __str__(self):
        # We return the playlist title.
        return self.title

