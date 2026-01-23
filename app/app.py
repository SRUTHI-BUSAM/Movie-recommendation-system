import streamlit as st
import pickle
import os
import sys

# --- Resolve paths safely ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(CURRENT_DIR, "..", "src")
MODELS_PATH = os.path.join(CURRENT_DIR, "..", "models")

sys.path.append(SRC_PATH)

from recommender import recommend

st.set_page_config(page_title="Movie Recommendation System")

st.title("🎬 Movie Recommendation System")

# --- Load model files safely ---
movies_path = os.path.join(MODELS_PATH, "movies.pkl")
similarity_path = os.path.join(MODELS_PATH, "similarity.pkl")

movies = pickle.load(open(movies_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie you like", movie_list)

if st.button("Recommend"):
    recommendations = recommend(selected_movie, movies, similarity)
    st.subheader("Recommended Movies")
    for movie in recommendations:
        st.write("👉", movie)
