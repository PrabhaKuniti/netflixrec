import streamlit as st
import pandas as pd
import numpy as np
import os

# Set page config for responsive layout
st.set_page_config(page_title="Netflix Recommendation System", layout="wide")

# Apply Netflix-like background styling with animations and responsive design
st.markdown(
    """
    <style>
        @keyframes fadeInZoom {
            from { opacity: 0; transform: scale(0.8); }
            to { opacity: 1; transform: scale(1); }
        }
        
        body {
            background-color: #141414;
            color: white;
            margin: 0;
            padding: 0;
            width: 100vw;
            height: 100vh;
        }
        .stApp {
            background-color: #141414;
            width: 100%;
        }
        .stTextInput, .stSelectbox, .stRadio, .stMarkdown {
            font-size: clamp(14px, 2vw, 18px);
            color: white !important;
        }
        .css-1v3fvcr, .css-2trqyj {
            background-color: #e50914 !important;
            color: white !important;
            border-radius: 8px;
        }
        .stDataFrame {
            background-color: #181818;
            color: white !important;
            border-radius: 8px;
            padding: 5px;
            font-size: clamp(12px, 2vw, 16px);
        }
        label, .stRadio label, .stRadio div {
            color: white !important;
        }
        
        .title-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 5vh 5vw;
        }
        
        .title-image {
            max-width: 80%;
            width:250px;
            height: auto;
            animation: fadeInZoom 2s ease-in-out;
        }
        
        .subtitle {
            font-size: clamp(20px, 4vw, 50px);
            color: #e50914;
            font-weight:Bold;
            text-align: center;
            animation: fadeInZoom 1.5s ease-in-out;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Display title image and subtitle
st.markdown("""
    <div class='title-container'>
        <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Netflix_2015_logo.svg" class='title-image'>
        <div class='subtitle'>Recommendation System</div>
    </div>
    """, unsafe_allow_html=True)

# Load Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load similarity matrices
movies_sim = np.load(os.path.join(BASE_DIR, 'movies_sim.npz'), allow_pickle=True)["m"]
tv_sim = np.load(os.path.join(BASE_DIR, 'tv_sim.npz'), allow_pickle=True)["t"]

# Load CSV datasets
movies_df = pd.read_csv(os.path.join(BASE_DIR, "movies_df.csv"))
tv_show = pd.read_csv(os.path.join(BASE_DIR, "tv_show.csv"))

# Extract movie and TV show titles
movie_titles = movies_df['title'].tolist()
tv_titles = tv_show['title'].tolist()

def recommend(title):
    if title in movies_df['title'].values:
        movies_index = movies_df[movies_df['title'] == title].index.item()
        scores = dict(enumerate(movies_sim[movies_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        selected_movies_index = list(sorted_scores.keys())[1:6]  # Skipping the first one
        rec_movies = movies_df.iloc[selected_movies_index].copy()
        rec_movies['similarity'] = list(sorted_scores.values())[1:6]
        return rec_movies[['title', 'country', 'genres', 'description', 'release_year', 'cast']]

    elif title in tv_show['title'].values:
        tv_index = tv_show[tv_show['title'] == title].index.item()
        scores = dict(enumerate(tv_sim[tv_index]))
        sorted_scores = dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))

        selected_tv_index = list(sorted_scores.keys())[1:6]
        rec_tv = tv_show.iloc[selected_tv_index].copy()
        rec_tv['similarity'] = list(sorted_scores.values())[1:6]
        return rec_tv[['title', 'country', 'genres', 'description', 'release_year', 'cast']]

    else:
        return None

# Streamlit UI
st.markdown("### Select a category:", unsafe_allow_html=True)
option = st.radio("", ("Movies", "TV Shows"))

if option == "Movies":
    title = st.selectbox("Enter a Movie Name", movie_titles, index=None)
elif option == "TV Shows":
    title = st.selectbox("Enter a TV Show Name", tv_titles, index=None)

if st.button("Get Recommendations"):
    if title:
        recommendations = recommend(title)
        if recommendations is not None:
            st.markdown("### Recommended Titles:", unsafe_allow_html=True)
            st.dataframe(recommendations)
        else:
            st.warning("Title not found! Try another one.")
    else:
        st.error("Please enter a valid movie or TV show name.")
