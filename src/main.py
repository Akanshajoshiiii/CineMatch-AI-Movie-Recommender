# app.py
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details

# Secure API key access
OMDB_API_KEY = st.secrets["OMDB_API_KEY"]

# Page setup
st.set_page_config(
    page_title="🎬 CineMatch AI",
    page_icon="🍿",
    layout="wide"
)

# ---------- 🔥 Custom CSS ----------
st.markdown("""
    <style>
    .movie-card {
        background-color: #1c1c1e;
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(255, 255, 255, 0.05);
        transition: 0.3s;
        margin-bottom: 20px;
    }
    .movie-card:hover {
        transform: scale(1.02);
        box-shadow: 0 0 25px rgba(255, 255, 255, 0.15);
    }
    .movie-title {
        font-size: 24px;
        font-weight: bold;
        color: #ff4757;
        margin-bottom: 8px;
    }
    .movie-plot {
        color: #dcdcdc;
        font-size: 16px;
        line-height: 1.5;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- 🎬 App Title ----------
st.markdown("<h1 style='color:#ff6b81;'>🍿 CineMatch - AI Movie Recommender</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='color:gray;'>Find your next favorite film in seconds 🎥</h4>", unsafe_allow_html=True)

# ---------- 🎯 Movie Selector ----------
movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎯 Select a movie you like:", movie_list)

# ---------- 🚀 Recommend Button ----------
if st.button("✨ Recommend Similar Movies"):
    with st.spinner("Crunching cinematic numbers..."):
        recommendations = recommend_movies(selected_movie)

        if recommendations is None or recommendations.empty:
            st.warning("❌ No recommendations found.")
        else:
            st.subheader("🔎 Here’s what you might love:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/150x220?text=No+Poster", use_container_width=True)
                    with col2:
                        st.markdown(f'<div class="movie-title">{movie_title}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="movie-plot">{plot if plot != "N/A" else "Plot not available."}</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
