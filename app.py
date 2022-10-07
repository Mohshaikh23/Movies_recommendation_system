import streamlit as st
import pickle
import pandas as pd
import requests

movie_list = pickle.load(open('movies.pkl','rb'))

movie_dict = movie_list.to_dict()

movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title('MOVIES RECOMMENDER SYSTEM')

select_movie_name  = st.selectbox('Select movie you want recommendation for', movies['title'].values)

def recommend(movie):

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies_poster = []
    recommended_movies = []

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        #Fetching movies
        recommended_movies.append(movies.iloc[i[0]].title)

        # Fetching movies-poster
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_poster

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=00852c939cf59d1b8a2c8d3aa679d889&language=en-US'.format(movie_id))
    data = response.json()
    return  'http://image.tmdb.org/t/p/w500/'+ data['poster_path']

if st.button('Recommend'):

    names, posters = recommend(select_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.header(names[0])
        st.image(posters[0])

    with col2:
        st.header(names[1])
        st.image(posters[1])

    with col3:
        st.header(names[2])
        st.image(posters[2])

    with col4:
        st.header(names[3])
        st.image(posters[3])

    with col5:
        st.header(names[4])
        st.image(posters[4])

