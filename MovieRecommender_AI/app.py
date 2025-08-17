# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# #other api=8265bd1679663a7ea12ac168da84d2e8
#
# def fetch_poster(movie_id):
#    response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=0a1fd0e161997679c6d838e934e6f841&language=en-US'.format(movie_id))
#    data=response.json()
#    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']
#
#
#
# def recommend(movie):
#     movie_index=movies[movies['title']==movie].index[0]
#     distances=similarity[movie_index]
#     movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
#
#     recommended_movies=[]
#     recommended_movies_posters=[]
#     for i in movies_list:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         # fetch poster from api
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_posters
#
# movies_dict=pickle.load(open('movie_dict.pkl', 'rb'))
# movies=pd.DataFrame(movies_dict)
# similarity=pickle.load(open('similarity.pkl', 'rb'))
#
# st.title('Movie Recommender System')
# selected_movie_name = st.selectbox ('Movie recommendation',movies['title'].values)
# if st.button('Recommend'):
#     names,posters= recommend(selected_movie_name)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(names[0])
#         st.image(posters[0])
#     with col2:
#         st.text(names[1])
#         st.image(posters[1])
#
#     with col3:
#         st.text(names[2])
#         st.image(posters[2])
#     with col4:
#         st.text(names[3])
#         st.image(posters[3])
#     with col5:
#         st.text(names[4])
#         st.image(posters[4])

import streamlit as st
import pickle
import pandas as pd
import requests

# You can use either API key
API_KEY = "0a1fd0e161997679c6d838e934e6f841"
# Alternative: API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# Function to fetch movie posters using TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=10)  # added timeout
        response.raise_for_status()  # raises HTTPError for bad responses
        data = response.json()
        if "poster_path" in data and data["poster_path"] is not None:
            return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"  # fallback
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error"

# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load movie data and similarity matrix
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('🎬 Movie Recommender System')
selected_movie_name = st.selectbox('Select a movie to get recommendations:', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    cols = st.columns(5)  # ✅ updated from beta_columns
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])
