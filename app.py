import requests
import pickle
import streamlit as st  # Import Streamlit

# Function to download pickle file from Google Drive
def download_pickle_from_gdrive(url):
    # Convert Google Drive URL to a direct download URL
    file_id = url.split('/d/')[1].split('/')[0]
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    # Send request to download the file
    response = requests.get(download_url, stream=True)
    
    # Check if the response is valid (200 OK)
    if response.status_code == 200:
        # Define the temporary path for the pickle file in the /tmp directory
        file_path = '/tmp/temp.pkl'  # The file will be used during the session
        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return file_path
    else:
        print(f"Failed to download the file: {response.status_code}")
        return None

# URLs for Google Drive pickle files (update these with your actual URLs)
df_url = "https://drive.google.com/file/d/your_file_id_1/view?usp=sharing"
similarity_url = "https://drive.google.com/file/d/your_file_id_2/view?usp=sharing"

# Download the pickle files
df_file_path = download_pickle_from_gdrive(df_url)
similarity_file_path = download_pickle_from_gdrive(similarity_url)

# Verify the downloaded content before unpickling
if df_file_path and similarity_file_path:
    try:
        with open(df_file_path, 'rb') as f:
            print(f.read(10))  # Read first 10 bytes to check content
        with open(similarity_file_path, 'rb') as f:
            print(f.read(10))  # Read first 10 bytes to check content
        
        # Load the pickle files
        df = pickle.load(open(df_file_path, 'rb'))
        similarity = pickle.load(open(similarity_file_path, 'rb'))
    except Exception as e:
        print(f"Error while unpickling: {e}")
else:
    print("Error: Could not download files.")

# Streamlit interface
st.header('Music Recommender System')
music_list = df['song'].values  # Make sure df contains the correct data
selected_music = st.selectbox("Type or select a song from the dropdown", music_list)


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
