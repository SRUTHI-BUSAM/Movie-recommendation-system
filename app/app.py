import streamlit as st
import pickle
import os
import sys
import requests


TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def fetch_movie_details(movie_name):
    try:
        api_key = TMDB_API_KEY

        url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

        response = requests.get(url, timeout=10)
        data = response.json()

        if "results" in data and data["results"]:
            movie = data["results"][0]

            poster = (
                "https://image.tmdb.org/t/p/w500" + movie["poster_path"]
                if movie["poster_path"]
                else None
            )

            return {
                "poster": poster,
                "rating": movie["vote_average"],
                "overview": movie["overview"],
                "release_date": movie["release_date"],
                "genre_ids": movie["genre_ids"]
            }

    except Exception as e:
        st.error(f"TMDB Error: {e}")
        return None

    return None

def fetch_trailer(movie_name):

    api_key =TMDB_API_KEY

    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={movie_name}"

    movie_data = requests.get(search_url, timeout=10).json()

    if "results" in movie_data and movie_data["results"]:

        movie_id = movie_data["results"][0]["id"]

        trailer_url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={api_key}"

        videos = requests.get(trailer_url, timeout=10).json()

        for video in videos["results"]:

            if video["site"] == "YouTube":

                return f"https://www.youtube.com/watch?v={video['key']}"

    return None


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(CURRENT_DIR, "..", "src")
MODELS_PATH = os.path.join(CURRENT_DIR, "..", "models")

sys.path.append(SRC_PATH)

from recommender import recommend

st.set_page_config(page_title="Movie Recommendation System")
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
}

div[data-testid="stVerticalBlock"] {
    border-radius: 10px;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

st.title("🎬 Movie Recommendation System")
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []
if "recommendations" not in st.session_state:
    st.session_state.recommendations = []
st.sidebar.title(
    f"❤️ My Watchlist ({len(st.session_state.watchlist)})"
)

for saved_movie in st.session_state.watchlist:

    col1, col2 = st.sidebar.columns([3,1])

    col1.write(saved_movie)

    if col2.button("❌", key=f"remove_{saved_movie}"):

        st.session_state.watchlist.remove(saved_movie)

        st.rerun()

movies_path = os.path.join(MODELS_PATH, "movies.pkl")
similarity_path = os.path.join(MODELS_PATH, "similarity.pkl")

movies = pickle.load(open(movies_path, "rb"))
similarity = pickle.load(open(similarity_path, "rb"))

movie_list = movies['title'].values

search_movie = st.text_input(
    "🔍 Search Movie"
)

filtered_movies = [
    movie for movie in movie_list
    if search_movie.lower() in movie.lower()
] if search_movie else movie_list

selected_movie = st.selectbox(
    "Select Movie",
    filtered_movies
)
if st.button("Recommend"):

    st.session_state.recommendations = recommend(
        selected_movie,
        movies,
        similarity
    )

recommendations = st.session_state.recommendations

if recommendations:

    st.subheader("🎯 Recommended Movies")

    cols = st.columns(len(recommendations))

    for idx, (movie, match_score) in enumerate(recommendations):

        details = fetch_movie_details(movie)

        if details:

            with cols[idx]:

                if details["poster"]:
                    st.image(details["poster"])

                st.markdown(
                    f"<p style='text-align:center; font-size:18px; font-weight:bold;'>{movie}</p>",
                    unsafe_allow_html=True
                )

                st.write(f"⭐ {details['rating']:.1f}")

                st.write(f"🔥 {match_score:.1f}% Match")

                year = details["release_date"][:4]
                st.write(f"📅 {year}")
                if st.button("ℹ Info", key=f"info_{idx}"):

                    st.session_state.selected_movie = movie
                trailer = fetch_trailer(movie)

                if trailer:
                    st.link_button(
                        "▶ Trailer",
                        trailer
                    )

                if st.button(f"❤️ Save", key=f"save_{idx}"):

                    if movie not in st.session_state.watchlist:

                        st.session_state.watchlist.append(movie)

                        st.success(f"{movie} added!")

                        st.rerun()
# ---------- Movie Details Section ----------

if st.session_state.get("selected_movie"):

    details = fetch_movie_details(
        st.session_state.selected_movie
    )

    if details:

        st.divider()

        st.subheader("🎬 Movie Details")

        col1, col2 = st.columns([1, 2])

        with col1:

            if details["poster"]:
                st.image(details["poster"])

        with col2:

            st.subheader(st.session_state.selected_movie)

            st.write(f"⭐ Rating: {details['rating']:.1f}")

            year = details["release_date"][:4]

            st.write(f"📅 Year: {year}")

            st.write(details["overview"])
