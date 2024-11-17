
import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

# Spotify API credentials
CLIENT_ID = "b9ddf09b18e7422f8996873e37446473"
CLIENT_SECRET = "c4b4ee4f1fc144f48754df477af4367b"

# Initialize Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def download_pickle_from_gdrive(url):
    # Download file from Google Drive
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to download the file. Please check the URL or your internet connection.")
        return None
    file_path = '/tmp/temp.pkl'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

# Google Drive URLs for your files
df_url  = "https://drive.google.com/uc?export=download&id=1pDEio0oeXQqkt4o8RDzodGvv-TTWtjfV"
similarity_url = "https://drive.google.com/uc?export=download&id=1ih8qAgx_VCNKuJaKmS7ma7PDJtfNLmnS"

# Download and load the pickle files
df_file_path = download_pickle_from_gdrive(df_url)
similarity_file_path = download_pickle_from_gdrive(similarity_url)

if df_file_path and similarity_file_path:
    try:
        music = pickle.load(open(df_file_path, 'rb'))
        similarity = pickle.load(open(similarity_file_path, 'rb'))
    except Exception as e:
        st.error(f"Error loading pickle files: {e}")
        st.stop()
else:
    st.stop()

# Check if the 'song' column exists in the loaded data
if 'song' not in music.columns:
    st.error("The data could not be loaded or is missing the 'song' column.")
    st.stop()

def recommend(song):
    try:
        index = music[music['song'] == song].index[0]
    except IndexError:
        st.error("Song not found in the dataset.")
        return [], []
    
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []

    for i in distances[1:11]:  # Get top 10 recommendations
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

# Streamlit app layout
st.header('Music Recommender System')
music_list = music['song'].values
selected_music = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)

    cols = st.columns(10)
    for col, name, poster in zip(cols, recommended_music_names, recommended_music_posters):
        with col:
            st.text(name)
            st.image(poster)
