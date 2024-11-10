import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests  # Import requests to download files

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
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def download_pickle_from_gdrive(url):
    response = requests.get(url)
    file_path = '/tmp/temp.pkl'
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

# URLs to your Google Drive files (replace with your actual URLs)
df_url = "YOUR_GOOGLE_DRIVE_URL_FOR_DF"
similarity_url = "YOUR_GOOGLE_DRIVE_URL_FOR_SIMILARITY"

# Download the pickle files
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
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)

    return recommended_music_names, recommended_music_posters

st.header('Music Recommender System')
music_list = music['song'].values
selected_music = st.selectbox(
    "Type or select a song from the dropdown",
    music_list
)

if st.button('Show Recommendation'):
    recommended_music_names, recommended_music_posters = recommend(selected_music)
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)

    with col1:
        st.text(recommended_music_names[0])
        st.image(recommended_music_posters[0])
    with col2:
        st.text(recommended_music_names[1])
        st.image(recommended_music_posters[1])
    with col3:
        st.text(recommended_music_names[2])
        st.image(recommended_music_posters[2])
    with col4:
        st.text(recommended_music_names[3])
        st.image(recommended_music_posters[3])
    with col5:
        st.text(recommended_music_names[4])
        st.image(recommended_music_posters[4])
    with col6:
        st.text(recommended_music_names[5])
        st.image(recommended_music_posters[5])
    with col7:
        st.text(recommended_music_names[6])
        st.image(recommended_music_posters[6])
    with col8:
        st.text(recommended_music_names[7])
        st.image(recommended_music_posters[7])
    with col9:
        st.text(recommended_music_names[8])
        st.image(recommended_music_posters[8])
    with col10:
        st.text(recommended_music_names[9])
        st.image(recommended_music_posters[9])
s