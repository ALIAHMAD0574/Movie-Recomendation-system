import streamlit as st
import pickle
import pandas as pd
import requests
import json

movies_list = pickle.load(open('movies_dict.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

def fetch_poster(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI4ODAxZTU0MWYyYWEzMzM5Yjk3MDAwMjcyMTc1MGEyZCIsIm5iZiI6MTcyMDk4NjM1Ni4zODczMzQsInN1YiI6IjY2OTQyOTJjZmU5NTgxOWM2NDAyNzY2NyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.HNNz0yxjXG4BJTLHD1A5P8ttq0kwBKvD-eA9EACunAM"
    }
    response = requests.get(url, headers=headers)
    try:
        poster_path = 'https://image.tmdb.org/t/p/w500/'+response.json()['poster_path']
    except:
        poster_path= 'https://static.streamlit.io/examples/owl.jpg'
    return poster_path

def recommend(movies_list,movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list_change = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies  = []
    recommended_movies_poster = []
    for i in movies_list_change:
        moview_id = movies_list.iloc[i[0]].movie_id
        recommended_movies_poster.append(fetch_poster(moview_id))
        recommended_movies.append(movies_list.iloc[i[0]].title)
    return recommended_movies,recommended_movies_poster



movies_list = pd.DataFrame(movies_list)
st.title('Movie Recommendation System')

slected_movie_option = st.selectbox(
    "How would you like to be contacted?",
    movies_list['title'].values)

if st.button("Recommend"):
    st.write("You selected:", slected_movie_option)
    names,posters = recommend(movies_list,slected_movie_option)
    columns = st.columns(5)
    # Loop through names and posters and distribute them across the columns
    for index, name in enumerate(names):
        col_index = index % 5  # Determine the column index
        with columns[col_index]:
            st.text(name)
            st.image(posters[index])


