import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from scipy.spatial.distance import cdist
from collections import defaultdict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import warnings

# Ignore warnings to keep the output clean
warnings.filterwarnings("ignore")

# Read input data
music_data = pd.read_csv("./input/data.csv")
genre_data = pd.read_csv('./input/data_by_genres.csv')
year_data = pd.read_csv('./input/data_by_year.csv')
artist_data = pd.read_csv('./input/data_by_artist.csv')

# Add a decade column to the music data
music_data['decade'] = music_data['year'].apply(lambda year: f'{(year//10)*10}s')

# Pipeline for genre clustering
genre_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=12))])
X_genre = genre_data.select_dtypes(np.number)
genre_pipeline.fit(X_genre)
genre_data['cluster'] = genre_pipeline.predict(X_genre)

# Pipeline for song clustering
song_pipeline = Pipeline([('scaler', StandardScaler()), ('kmeans', KMeans(n_clusters=25, verbose=False))], verbose=False)
X_songs = music_data.select_dtypes(np.number)
song_pipeline.fit(X_songs)
song_labels = song_pipeline.predict(X_songs)
music_data['cluster_label'] = song_labels

# Spotify API credentials
CLIENT_ID = "c64c6716a26b451ab6c8d0efcb9954ec"
CLIENT_SECRET = "1b58055aa6744ed68c9352e9730f6fae"

# Authenticate with the Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))

# Function to find a track using Spotify API
def find_track(track_name, track_year, track_artist):
    track_info = defaultdict()
    results = sp.search(q='track: "{}" artist: "{}" year: {}'.format(track_name, track_artist, track_year), limit=1)
    if not results['tracks']['items']:
        return None

    results = results['tracks']['items'][0]
    track_id = results['id']
    audio_features = sp.audio_features(track_id)[0]

    # Extract track information
    track_info['name'] = [track_name]
    track_info['year'] = [track_year]
    track_info['artist'] = [track_artist]
    track_info['explicit'] = [int(results['explicit'])]
    track_info['duration_ms'] = [results['duration_ms']]
    track_info['popularity'] = [results['popularity']]

    # Extract audio features
    for key, value in audio_features.items():
        track_info[key] = value

    return pd.DataFrame(track_info)

# List of numerical features for analysis
numerical_features = ['valence', 'year', 'acousticness', 'danceability', 'duration_ms', 'energy', 'explicit',
                      'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'popularity', 'speechiness', 'tempo']

# Function to retrieve track data from either local dataset or Spotify API
def get_track_data(track, data_source):
    try:
        track_data = data_source[(data_source['name'] == track['name']) &
                                 (data_source['year'] == track['year']) &
                                 (data_source['artists'] == track['artists'])]
        if not track_data.empty:
            print('Fetching track information from local dataset')
            return track_data.iloc[0]
    except IndexError:
        pass
    print('Fetching track information from Spotify API')
    return find_track(track['name'], track['year'], track['artists'])

# Function to calculate the mean vector for a list of tracks
def get_average_vector(track_list, data_source):
    track_vectors = []
    for track in track_list:
        track_data = get_track_data(track, data_source)
        if track_data is None:
            print('Warning: {} does not exist in the database'.format(track['name']))
            continue
        track_vector = track_data[numerical_features].values
        track_vectors.append(track_vector)

    track_matrix = np.array(list(track_vectors))
    return np.mean(track_matrix, axis=0)

# Function to flatten a list of dictionaries into a single dictionary
def flatten_dictionary_list(dict_list):
    flattened_dict = defaultdict()
    for key in dict_list[0].keys():
        flattened_dict[key] = []
    for dic in dict_list:
        for key, value in dic.items():
            flattened_dict[key].append(value)
    return flattened_dict

# Function to recommend songs based on a list of input tracks
def recommend_songs(track_list, data_source, n_tracks=12):
    metadata_columns = ['name', 'year', 'artists']
    track_dict = flatten_dictionary_list(track_list)
    track_center = get_average_vector(track_list, data_source)
    scaler = song_pipeline.steps[0][1]
    scaled_data = scaler.transform(data_source[numerical_features])
    scaled_track_center = scaler.transform(track_center.reshape(1, -1))
    distances = cdist(scaled_track_center, scaled_data, 'cosine')
    index = list(np.argsort(distances)[:,:n_tracks][0])
    recommended_tracks = data_source.iloc[index]
    recommended_tracks = recommended_tracks[~recommended_tracks['name'].isin(track_dict['name'])]
    return recommended_tracks[metadata_columns].to_dict(orient='records')
