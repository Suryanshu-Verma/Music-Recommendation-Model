import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

CLIENT_ID = "b9ddf09b18e7422f8996873e37446473"
CLIENT_SECRET = "c4b4ee4f1fc144f48754df477af4367b"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")
    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        return track["album"]["images"][0]["url"]
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def download_pickle_from_gdrive(url):
    try:
        file_id = url.split('/d/')[1].split('/')[0]  # Standard link format
    except IndexError:
        file_id = url.split('id=')[1]  # Fallback for non-standard format
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(download_url)
    file_path = '/tmp/temp.pkl'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

# Google Drive URLs
df_url = "https://drive.google.com/file/d/1pDEio0oeXQqkt4o8RDzodGvv-TTWtjfV/view?usp=sharing"
similarity_url = "https://drive.google.com/file/d/1ih8qAgx_VCNKuJaKmS7ma7PDJtfNLmnS/view?usp=sharing"

# Download pickle files
df_file_path = download_pickle_from_gdrive(df_url)
similarity_file_path = download_pickle_from_gdrive(similarity_url)

# Load the pickle files
music = pickle.load(open(df_file_path, 'rb'))
similarity = pickle.load(open(similarity_file_path, 'rb'))

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    for i in distances[1:11]:  # Top 10 recommendations
        artist = music.iloc[i[0]].artist
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
    return recommended_music_names, recommended_music_posters

# Streamlit interface
st.header('Music Recommender System')
music_list = music['song'].values
selected_music = st.selectbox("Type or select a song from the dropdown", music_list)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)
    cols = st.columns(10)
    for i in range(10):
        with cols[i]:
            st.text(recommended_music_names[i])
            st.image(recommended_music_posters[i])
