# We import the serializers module from the rest_framework package.
# Serializers are like translators: they convert complex database rows into clean, readable JSON text,
# and they also validate incoming JSON requests to make sure they are safe and properly formatted before saving them.
from rest_framework import serializers

# We import our custom Genre, Song, Playlist, and Comment models.
from .models import Genre, Song, Playlist, Comment


# The GenreSerializer maps the Genre model to a JSON structure.
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


# The SongSerializer maps the Song model to a JSON structure.
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


# The PlaylistSerializer maps the Playlist model to a JSON structure.
# This version is kept extremely simple and beginner-friendly!
# It does not contain any complex custom methods or overrides.
class PlaylistSerializer(serializers.ModelSerializer):
    
    # We declare the genre field as nested. When we read a playlist,
    # it will show the full details of the Genre (id and name) instead of just the ID number.
    # We set 'read_only=True' because we will handle creating and linking the genre manually in our view!
    genre = GenreSerializer(read_only=True)
    
    # We declare the songs field as nested. When we read a playlist,
    # it will show the full list of songs with all their details (id, title, artist, duration).
    # We set 'read_only=True' because we will handle adding songs to the playlist manually in our view!
    songs = SongSerializer(many=True, read_only=True)

    class Meta:
        # We associate this translator with our Playlist database model.
        model = Playlist
        
        # We translate all fields (id, title, description, genre, songs).
        fields = '__all__'


# The CommentSerializer maps the Comment model to a JSON structure.
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        # We associate this translator with our Comment database model.
        model = Comment
        
        # We translate all fields (id, content, created_at, playlist).
        fields = '__all__'
