import requests
import pickle
import streamlit as st

# Function to download pickle file from Google Drive
def download_pickle_from_gdrive(url):
    file_id = url.split('/d/')[1].split('/')[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(download_url, stream=True)
    if response.status_code == 200:
        file_path = '/tmp/temp.pkl'
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return file_path
    else:
        st.error(f"Failed to download file from Google Drive. Status code: {response.status_code}")
        return None

# Updated URLs for Google Drive pickle files
df_url = "https://drive.google.com/file/d/1pDEio0oeXQqkt4o8RDzodGvv-TTWtjfV/view?usp=sharing"
similarity_url = "https://drive.google.com/file/d/1ih8qAgx_VCNKuJaKmS7ma7PDJtfNLmnS/view?usp=sharing"

# Download the pickle files
df_file_path = download_pickle_from_gdrive(df_url)
similarity_file_path = download_pickle_from_gdrive(similarity_url)

# Load data if downloads were successful
if df_file_path and similarity_file_path:
    try:
        with open(df_file_path, 'rb') as f:
            df = pickle.load(f)
        with open(similarity_file_path, 'rb') as f:
            similarity = pickle.load(f)
    except Exception as e:
        st.error(f"Error while unpickling: {e}")
else:
    st.error("Error: Could not download files.")

# Streamlit interface setup
st.header('Music Recommender System')

# Proceed only if 'df' is loaded successfully
if 'df' in locals() and 'song' in df.columns:
    music_list = df['song'].values
    selected_music = st.selectbox("Type or select a song from the dropdown", music_list)

    # Recommendation function
    def recommend(song):
        index = df[df['song'] == song].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_music_names = []
        recommended_music_posters = []
        for i in distances[1:11]:
            artist = df.iloc[i[0]].artist
            recommended_music_names.append(df.iloc[i[0]].song)
            recommended_music_posters.append("URL to album cover")  # Placeholder URL
        return recommended_music_names, recommended_music_posters

    # Show recommendations if a song is selected
    if st.button('Show Recommendation'):
        recommended_music_names, recommended_music_posters = recommend(selected_music)
        cols = st.columns(10)
        for i in range(10):
            with cols[i]:
                st.text(recommended_music_names[i])
                st.image(recommended_music_posters[i], width=100)
else:
    st.error("The data could not be loaded or is missing the 'song' column.")
