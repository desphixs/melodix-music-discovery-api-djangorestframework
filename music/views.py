# We import standard rendering and lookup shortcuts from Django.
from django.shortcuts import render, get_object_or_404
# We import Paginator and EmptyPage from django's core pagination package to page our song listings manually.
from django.core.paginator import Paginator, EmptyPage
# We import the core class APIView from rest_framework.views.
# APIView is the rawest form of class-based view provided by DRF, letting us build clean GET and POST methods.
from rest_framework.views import APIView
# We import the custom Response class from rest_framework.response.
# This wraps standard JSON returns in a nice, professional API interface.
from rest_framework.response import Response
# We import HTTP status code constants (like 200 OK, 201 Created, 400 Bad Request).
from rest_framework import status

# We import our database models and their respective serializers.
from .models import Genre, Song, Playlist, Comment
from .serializers import GenreSerializer, SongSerializer, PlaylistSerializer, CommentSerializer


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


# This class-based view manages listing all playlists and creating new ones.
# It inherits from DRF's APIView to give us raw control over GET and POST methods.
class PlaylistListAPIView(APIView):
    
    # The get method fetches every single playlist in the database, with optional search filtering.
    def get(self, request):
        # We start by fetching a base queryset of all playlists from our database.
        playlists = Playlist.objects.all()
        
        # 1. We extract the optional 'genre' search term from the URL query parameters.
        # For example, in /api/playlists/?genre=chill, genre_query will be "chill".
        genre_query = request.query_params.get('genre')
        
        # 2. We extract the optional 'song' search term from the URL query parameters.
        # For example, in /api/playlists/?song=midnight, song_query will be "midnight".
        song_query = request.query_params.get('song')
        
        # 3. If a genre query term was typed by the user, we filter our playlists.
        if genre_query:
            # We filter the playlists where the linked genre's name contains the search term.
            # '__icontains' makes the search case-insensitive, meaning "CHILL" and "chill" match the same way!
            playlists = playlists.filter(genre__name__icontains=genre_query)
            
        # 4. If a song query term was typed by the user, we filter our playlists.
        if song_query:
            # We filter playlists containing any song whose title contains the search term case-insensitively.
            playlists = playlists.filter(songs__title__icontains=song_query)
            
        # 5. When we query across Many-to-Many relationships (like songs in a playlist),
        # Django generates SQL JOIN statements that can return duplicate rows for a single playlist.
        # Calling .distinct() makes sure that each unique playlist is returned exactly once in our list!
        playlists = playlists.distinct()
        
        # We serialize the filtered collection of playlists.
        # 'many=True' tells our PlaylistSerializer to loop through and translate a list of objects.
        serializer = PlaylistSerializer(playlists, many=True)
        
        # We return the translated JSON data to the client with a 200 OK code.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # The post method manually handles extracting fields, looking up relationships, and saving the playlist.
    def post(self, request):
        # 1. We manually extract the parameters from request.data
        title = request.data.get('title')
        description = request.data.get('description', '')
        genre_id = request.data.get('genre')
        song_ids = request.data.get('songs', [])

        # 2. Explicit validation check: Ensure vital required fields are present
        if not title:
            # If the title is missing, we return a customized bad request error dict.
            return Response({"title": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
        if not genre_id:
            # If the genre is missing, we return a customized bad request error dict.
            return Response({"genre": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)

        # 3. Look up the Genre object from our database
        try:
            # We fetch the specific genre row matching the provided ID number.
            genre = Genre.objects.get(id=genre_id)
        except Genre.DoesNotExist:
            # If the ID does not exist in the database, we return a clear validation error.
            return Response({"genre": ["Genre not found."]}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Create and save the core Playlist record in the database.
        # We assign the fetched Genre instance directly to our ForeignKey field!
        playlist = Playlist.objects.create(
            title=title,
            description=description,
            genre=genre
        )

        # 5. Fetch all matching Song rows from the database using their ID numbers.
        # The id__in lookup works like SQL's IN operator (e.g., SELECT * FROM songs WHERE id IN (1, 2, 3)).
        songs_from_db = Song.objects.filter(id__in=song_ids)

        # 6. Establish the Many-to-Many connections inside the secret join table.
        # The .songs.set() helper handles writing the correct links into the mapping table automatically.
        playlist.songs.set(songs_from_db)

        # 7. Translate the completed playlist record.
        # Because we configured read-only nested serializers inside PlaylistSerializer,
        # it will automatically render the full genre details and song lists in our JSON response!
        serializer = PlaylistSerializer(playlist)
        
        # We return the saved record inside our Response along with a "201 Created" success status.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# This class-based view handles displaying details of a single Playlist with paginated songs.
class PlaylistDetailAPIView(APIView):
    
    # The get method fetches a specific playlist by its ID and manually pages its tracklist.
    def get(self, request, pk):
        # 1. Fetch the specific playlist by its unique primary key ID.
        # If the playlist doesn't exist, we raise a clean 404 Not Found error automatically.
        playlist = get_object_or_404(Playlist, id=pk)
        
        # 2. Extract the 'page' and 'size' parameters from the GET request URL query parameters.
        # For example, in /api/playlists/1/?page=2&size=3, we read page=2 and size=3.
        # We wrap these in a try/except block to handle invalid strings and default them safely.
        try:
            page_number = int(request.query_params.get('page', 1))
        except ValueError:
            page_number = 1
            
        try:
            page_size = int(request.query_params.get('size', 5))
        except ValueError:
            page_size = 5

        # 3. Retrieve all Song objects associated with this specific playlist.
        # We order them by their unique 'id' to ensure pagination order is always stable.
        songs_queryset = playlist.songs.all().order_by('id')

        # 4. Use Django's built-in Paginator tool to slice and organize our song collection.
        # We pass our full songs query and the desired count of items per page.
        paginator = Paginator(songs_queryset, page_size)

        # 5. Extract the specific page requested by the client.
        try:
            page_obj = paginator.page(page_number)
        except EmptyPage:
            # If the user requests an empty page (like page 999), we assign an empty page slice.
            page_obj = []

        # 6. Serialize our playlist details and paginated songs separately.
        # This keeps our logic extremely explicit and transparent!
        paginated_songs_data = SongSerializer(page_obj, many=True).data

        # 7. Construct a custom dictionary response combining base details and page metadata.
        response_data = {
            "id": playlist.id,
            "title": playlist.title,
            "description": playlist.description,
            # We serialize the single genre object to show full nested info (id and name)
            "genre": GenreSerializer(playlist.genre).data,
            
            # Metadata block detailing exactly how pages are mapped
            "pagination": {
                "total_songs": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page_number,
                "page_size": page_size,
                "has_next": page_obj.has_next() if hasattr(page_obj, 'has_next') else False,
                "has_previous": page_obj.has_previous() if hasattr(page_obj, 'has_previous') else False,
            },
            
            # The paginated song array
            "songs": paginated_songs_data
        }

        # We return the compiled response dictionary with a standard 200 OK status.
        return Response(response_data, status=status.HTTP_200_OK)


# This class-based view manages collaborative comments linked to a specific playlist.
class PlaylistCommentsAPIView(APIView):
    
    # The get method fetches all comments belonging to a specific playlist.
    def get(self, request, playlist_id):
        # 1. Fetch the specific playlist by its unique ID.
        # If it doesn't exist, we immediately return a clean 404 response.
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # 2. Retrieve all Comment records associated with this specific playlist.
        # We order them by 'created_at' in ascending order so comments appear in thread order!
        comments = playlist.comments.all().order_by('created_at')
        
        # 3. Serialize the list of comment objects.
        # 'many=True' tells our CommentSerializer to translate a list of objects.
        serializer = CommentSerializer(comments, many=True)
        
        # We return the translated list inside a standard Response with a 200 OK status.
        return Response(serializer.data, status=status.HTTP_200_OK)

    # The post method creates a new comment under a specific playlist.
    def post(self, request, playlist_id):
        # 1. Fetch the specific playlist by its unique ID.
        # If it doesn't exist, we return a 404 Not Found error.
        playlist = get_object_or_404(Playlist, id=playlist_id)
        
        # 2. Manually extract the comment fields from the incoming request.data payload.
        content = request.data.get('content')
        
        # 3. Explicit validation: Ensure the comment has actual text written in it!
        if not content or not content.strip():
            # If content is blank or missing, return a customized bad request error dict.
            return Response({"content": ["This field is required."]}, status=status.HTTP_400_BAD_REQUEST)
            
        # 4. Create and save the new Comment row in the database,
        # associating it directly with our verified Playlist object!
        comment = Comment.objects.create(
            playlist=playlist,
            content=content
        )
        
        # 5. Translate the newly created comment record into JSON format.
        serializer = CommentSerializer(comment)
        
        # We return the translated object with a "201 Created" success status.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


