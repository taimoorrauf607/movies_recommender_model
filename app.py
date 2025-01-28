import pandas as pd
import streamlit as st
import pickle

import requests
# load a movie names 
movies_dict = pickle.load(open('movie.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# load a similarity using pickle
similarity = pickle.load(open('similarity.pkl','rb'))

# fetch poster using TMDB Api
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# main recommend function

def recommend(movie):
    
    movie_index = movies[movies['title']==movie].index[0]
    distance =similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)),reverse=True,key=lambda x:x[1])[1:6]

    recommend_movie = []
    poster = []
    for i in movie_list:

        movie_id = movies.iloc[i[0]].id # movie_id is column
        # fetch poster from api
        poster.append(fetch_poster(movie_id))

        recommend_movie.append(movies.iloc[i[0]].title)  # title is column
    return recommend_movie , poster
    

st.title('Movies recommendation System')  # title on top

movie_list = movies['title'].values
selected_movie = st.selectbox (
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button("Recommend"):
    recommend_movie, poster = recommend(selected_movie)
    
    col1 , col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommend_movie[0])
        st.image(poster[0])
    with col2:
        st.text(recommend_movie[1])
        st.image(poster[1])
    with col3:
        st.text(recommend_movie[2])
        st.image(poster[2])
    with col4:
        st.text(recommend_movie[3])
        st.image(poster[3])
    with col5:
        st.text(recommend_movie[4])
        st.image(poster[4])