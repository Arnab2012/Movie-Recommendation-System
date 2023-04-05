import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommendation System')
movies=pickle.load(open('movies.pkl','rb')) # load the model
similarity=pickle.load(open('similarity.pkl','rb'))

movie=movies['title'].values # movie titles

# selecting Movie Name
option = st.selectbox(
    'Select Movie Name-->',
    movie)

# fetching posters
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# recommend function to get the movie name
def recommend(movie):
    ind=movies[movies['title']==movie].index[0]
    distances=similarity[ind]
    movie_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:11]
    recommended_movies=[]
    recommended_posters=[]
    for i in movie_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching posters
        recommended_posters.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies,recommended_posters


if st.button('Recommend'):
    st.write('Recommended Movies are-->')
    movie_name, movie_poster = recommend(option)
    n = len(movie_name)
    rows = n // 5 + min(n % 5, 1) # calculate number of rows needed
    for i in range(rows):
        row = st.columns(5)
        for j in range(min(n - i * 5, 5)):
            with row[j]:
                st.text(movie_name[i * 5 + j])
                st.image(movie_poster[i * 5 + j])