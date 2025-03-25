import streamlit as st
import requests
import pandas as pd
import pickle
import gdown
import gzip
import os

# 🎯 Google Drive file IDs (Replace these with your actual file IDs)
file_ids = {
    "movie_list.pkl.gz": "12ApWWR5UilG2_QbsOSYwg7sVVrv51VTn",
    "similarity.pkl.gz": "1I1wKUho-XlAq1NhWpp1VNiODSLjRZMoj"
}

# 📌 Download & extract files if they don’t exist
for file_name, file_id in file_ids.items():
    if not os.path.exists(file_name.replace(".gz", "")):
        gdown.download(f"https://drive.google.com/uc?id={file_id}", file_name, quiet=False)
        with gzip.open(file_name, "rb") as f_in:
            with open(file_name.replace(".gz", ""), "wb") as f_out:
                f_out.write(f_in.read())

# ✅ Load datasets
with open("movie_list.pkl", "rb") as f:
    movies = pickle.load(f)

with open("similarity.pkl", "rb") as f:
    similarity = pickle.load(f)

# ✅ Ensure movies is a DataFrame
movies = pd.DataFrame(movies)

# 🎬 TMDB API Key
API_KEY = "ec6689028c28f8828e66c8bffaa192d1"

def fetch_movie_details(movie_id):
    """Fetches poster, rating, and release year from TMDB API."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url).json()
        poster_url = f"https://image.tmdb.org/t/p/w500{response.get('poster_path')}" if response.get("poster_path") else "https://via.placeholder.com/300x450.png?text=No+Image"
        rating = response.get("vote_average", "N/A")
        year = response.get("release_date", "Unknown")[:4]
        return poster_url, rating, year
    except Exception:
        return "https://via.placeholder.com/300x450.png?text=No+Image", "N/A", "Unknown"

def recommend(movie):
    """Recommends similar movies based on cosine similarity."""
    if not movie:
        return []
    
    movie_index = movies[movies['title'] == movie].index
    if movie_index.empty:
        return []

    index = movie_index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1:11]:  # Get top 10 recommendations
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating, year = fetch_movie_details(movie_id)
        recommendations.append((movie_title, poster, rating, year))

    return recommendations

# 🎨 Streamlit UI
st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #FF5733;'>🎬 Movie Recommendation System 🎥</h1>
    <style>
        div[data-testid="stSelectbox"] label {color: #FF5733; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

selected_movie = st.selectbox("🔍 Search for a movie...", movies['title'].values, index=0)

if st.button("🔮 Show Recommendations"):
    if not selected_movie:
        st.warning("⚠️ Please select a movie before getting recommendations.")
    else:
        with st.spinner("Finding similar movies..."):
            recommended_movies = recommend(selected_movie)

        st.markdown("---")

        if recommended_movies:
            for i in range(0, len(recommended_movies), 5):
                cols = st.columns(5)
                for j, col in enumerate(cols):
                    if i + j < len(recommended_movies):
                        name, poster, rating, year = recommended_movies[i + j]
                        with col:
                            st.markdown(f"""
                                <div style="text-align: center;">
                                    <img src="{poster}" width="150" style="border-radius: 10px;"/>
                                    <p style="font-weight: bold; font-size: 16px; color: white;">{name}</p>
                                    <p style="color: gold; font-size: 14px;">⭐ IMDb: {rating}</p>
                                    <p style="color: lightgray; font-size: 12px;">📅 Year: {year}</p>
                                </div>
                            """, unsafe_allow_html=True)
        else:
            st.error("❌ No recommendations found for the selected movie.")
