# We import the serializers module from the rest_framework package.
# Serializers are like translators: they convert complex database rows into clean, readable JSON text,
# and they also validate incoming JSON requests to make sure they are safe and properly formatted before saving them.
from rest_framework import serializers

# We import our custom models from the models.py file.
from .models import Genre, Song

# The GenreSerializer maps the Genre model to a JSON structure.
# We inherit from ModelSerializer to let Django REST Framework write most of the boilerplate for us!
class GenreSerializer(serializers.ModelSerializer):
    # The Meta subclass holds configuration parameters for the serializer.
    class Meta:
        # We tell the serializer which database table it is translating.
        model = Genre
        
        # We define exactly which fields from the table we want to expose to our API.
        # '__all__' is a special shortcut that automatically includes all columns from the database table.
        fields = '__all__'


# The SongSerializer maps the Song model to a JSON structure.
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        # We associate this translator with our Song database model.
        model = Song
        
        # Again, we expose all of the columns (id, title, artist, duration) to our JSON output.
        fields = '__all__'
