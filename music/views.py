# We import the standard rendering tool from Django shortcuts.
from django.shortcuts import render
# We import the core class APIView from rest_framework.views.
# APIView is the rawest form of class-based view provided by DRF, letting us build clean GET and POST methods.
from rest_framework.views import APIView
# We import the custom Response class from rest_framework.response.
# This wraps standard JSON returns in a nice, professional API interface.
from rest_framework.response import Response
# We import HTTP status code constants (like 200 OK, 201 Created, 400 Bad Request).
from rest_framework import status

# We import our database models and their respective serializers.
from .models import Genre, Song
from .serializers import GenreSerializer, SongSerializer


# This class-based view manages the catalog of Genres.
# It supports listing existing genres (GET) and adding a new genre (POST).
class GenreListAPIView(APIView):
    
    # The get method handles all incoming HTTP GET requests to read the genre list.
    def get(self, request):
        # We query the database to fetch every single genre row saved.
        genres = Genre.objects.all()
        
        # We pass our list of genre records to our serializer.
        # 'many=True' is a parameter telling the serializer to loop through and translate a LIST of objects, not just one.
        serializer = GenreSerializer(genres, many=True)
        
        # We return the translated list inside a standard REST Framework Response.
        # This will render as a beautiful JSON list in the browser or terminal.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # The post method handles all incoming HTTP POST requests to create a new genre.
    def post(self, request):
        # We feed the raw incoming JSON data (located in request.data) into our translator.
        serializer = GenreSerializer(data=request.data)
        
        # We run the validation suite to make sure the data is correct, safe, and complies with unique settings.
        # If the check fails, Django REST Framework will raise a validation exception and stop execution here.
        if serializer.is_valid():
            # If the data is 100% correct, we write it as a new row to the database.
            serializer.save()
            
            # We return the newly created object along with a "201 Created" success status.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # If the validation failed, we return the error dictionary along with a "400 Bad Request" status.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# This class-based view manages the catalog of Songs.
# It supports listing all songs (GET) and creating new ones (POST).
class SongListAPIView(APIView):
    
    # The get method fetches the song catalog list.
    def get(self, request):
        # We pull all songs out of our database.
        songs = Song.objects.all()
        
        # We serialize the entire list of songs.
        serializer = SongSerializer(songs, many=True)
        
        # We return the serialized list to the client.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # The post method creates a new song entry.
    def post(self, request):
        # We populate the SongSerializer with the incoming data payload.
        serializer = SongSerializer(data=request.data)
        
        # We validate the song inputs (making sure title, artist, and duration are valid).
        if serializer.is_valid():
            # Save the new song to our SQL database table.
            serializer.save()
            
            # Return the saved song info with a "201 Created" response code.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        # Return validation errors back to the caller with a "400 Bad Request" code.
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
