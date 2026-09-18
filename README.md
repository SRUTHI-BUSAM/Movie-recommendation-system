# 🎬 Movie Recommendation System

A content-based Movie Recommendation System built using Python, Machine Learning, Streamlit, and the TMDB API.

The system recommends movies similar to the movie selected by the user using **TF-IDF vectorization** and **Cosine Similarity**. It also provides movie posters, ratings, release years, overviews, trailers, and a personal watchlist.

## 🚀 Live Demo

👉 [Movie Recommendation System](https://movie-recommendation-system-98mqukhjm7svn4ruu7hfnr.streamlit.app/)

## 📌 Features

- 🔍 Search for movies
- 🎬 Select a movie from the dataset
- 🎯 Get similar movie recommendations
- 📊 Content-based recommendation using TF-IDF
- 🔗 Cosine similarity for finding similar movies
- ⭐ Display TMDB movie ratings
- 🖼️ Display movie posters
- 📅 Display movie release year
- ℹ️ View movie overview and details
- ▶️ Watch movie trailers through YouTube
- ❤️ Add movies to a personal watchlist
- ❌ Remove movies from the watchlist
- ☁️ Deployed using Streamlit Community Cloud

## 🧠 How It Works

The recommendation system follows a content-based filtering approach.

```text
Movie Dataset
      ↓
Data Preprocessing
      ↓
Movie Tags
      ↓
TF-IDF Vectorization
      ↓
Movie Feature Vectors
      ↓
Cosine Similarity
      ↓
Find Similar Movies
      ↓
Top 4 Recommendations