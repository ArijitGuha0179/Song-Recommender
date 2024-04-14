### Dataset:

- data.csv: Main dataset containing song information.
- data_by_genres.csv: Dataset containing genre information.
- data_by_year.csv: Dataset containing year information.
- data_by_artist.csv: Dataset containing artist information.
- Make sure to place these files in the ```./input``` directory before running the code.

### Spotify API

- The system uses the Spotify API to retrieve song information that is not available in the local dataset. 
- To use the Spotify API, you need to create a Spotify Developer account and obtain the Client ID and Client Secret for your application. Update the ```CLIENT_ID``` and ```CLIENT_SECRET``` variables in the code with your credentials.

### Preprocess the data:
- Add a 'decade' column to the main dataset based on the 'year' column.
- Create a clustering pipeline for genre data and fit it to the genre dataset.
- Create a clustering pipeline for song data and fit it to the main dataset.
- Initialize the Spotify API client:
    ```python
    CLIENT_ID = "your_client_id"
    CLIENT_SECRET = "your_client_secret"
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
    ```
### Utility functions
- find_song: Retrieves song information from the Spotify API based on the provided song name, year, and artist.
- get_song_data: Retrieves song information from the local dataset or the Spotify API.
- get_mean_vector: Calculates the mean vector of a list of songs.
- flatten_dict_list: Flattens a list of dictionaries into a single dictionary.
### Recommendation function

- This function takes a list of seed songs, the Spotify dataset, and the desired number of recommendations as input. It returns a list of recommended songs based on the seed songs.
- Call the recommendation function with the desired input
```python
   def recommend_songs(song_list, spotify_data, n_songs=12):
        metadata_cols = ['name', 'year', 'artists']
        song_dict = flatten_dict_list(song_list)
        song_center = get_mean_vector(song_list, spotify_data)
        scaler = song_cluster_pipeline.steps[0][1]
        scaled_data = scaler.transform(spotify_data[number_cols])
        scaled_song_center = scaler.transform(song_center.reshape(1, -1))
        distances = cdist(scaled_song_center, scaled_data, 'cosine')
        index = list(np.argsort(distances)[:,:n_songs][0])
        rec_songs = spotify_data.iloc[index]
        rec_songs = rec_songs[~rec_songs['name'].isin(song_dict['name'])]
        return rec_songs[metadata_cols].to_dict(orient='records')
```
This will print the recommended songs based on the provided seed songs.

### Recommendation Algorithm

The recommendation algorithm works as follows:

- Preprocess the genre and song data using clustering techniques (KMeans) to create clusters of similar songs.
- For each seed song provided by the user:
   - Retrieve the song information from the local dataset or the Spotify API.
   - Calculate the mean vector of the song features.
   - Calculate the cosine distance between the mean vector of the seed songs and all the songs in the dataset.
   - Sort the songs based on the cosine distance and select the top n_songs recommendations.
   - Filter out any songs that are already present in the seed songs.
   - Return the recommended songs.
