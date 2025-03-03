import streamlit as st
import pandas as pd
import numpy as np
import os

# Set title of the app
st.title("🎬 Netflix Recommendation System")

# Load Data
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load similarity matrices
movies_sim = np.load(os.path.join(BASE_DIR, 'movies_sim.npz'), allow_pickle=True)["m"]
tv_sim = np.load(os.path.join(BASE_DIR, 'tv_sim.npz'), allow_pickle=True)["t"]

# Load CSV datasets
movies_df = pd.read_csv(os.path.join(BASE_DIR, "movies_df.csv"))
tv_show = pd.read_csv(os.path.join(BASE_DIR, "tv_show.csv"))

# Recommendation Function
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
title = st.text_input("Enter a Movie or TV Show Name")

if st.button("Get Recommendations"):
    if title:
        recommendations = recommend(title)
        if recommendations is not None:
            st.write("### Recommended Titles:")
            st.dataframe(recommendations)
        else:
            st.warning("Title not found! Try another one.")
    else:
        st.error("Please enter a valid movie or TV show name.")
