import pickle
import streamlit as st
import requests

API_KEY = "ec6689028c28f8828e66c8bffaa192d1"

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url).json()

    poster_url = f"https://image.tmdb.org/t/p/w500{response.get('poster_path')}" if response.get("poster_path") else "https://via.placeholder.com/300x450.png?text=No+Image"
    rating = response.get("vote_average", 0)  
    year = response.get("release_date", "Unknown")[:4]

    return poster_url, rating, year

def recommend(movie):
    if not movie:
        return []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)

    recommendations = []
    for i in distances[1:11]:  # Get top 10 recommendations
        movie_title = movies.iloc[i[0]].title
        movie_id = movies.iloc[i[0]].movie_id

        poster, rating, year = fetch_movie_details(movie_id)
        recommendations.append((movie_title, poster, rating, year))

    return recommendations

# Load datasets
movies = pickle.load(open(r'F:\XboxGames\artifacts\movie_list.pkl', 'rb'))
similarity = pickle.load(open(r'F:\XboxGames\artifacts\similarity.pkl', 'rb'))

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <h1 style='text-align: center; color: #FF5733;'>🎬 Movie Recommendation System 🎥</h1>
    <style>
        div[data-testid="stSelectbox"] label {color: #FF5733; font-weight: bold;}
    </style>
""", unsafe_allow_html=True)

selected_movie = st.selectbox("🔍 Search for a movie...", movies['title'].values, index=None)

if st.button("🔮 Show Recommendations"):
    with st.spinner("Finding similar movies..."):
        recommended_movies = recommend(selected_movie)

    st.markdown("---")
    
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
