import streamlit as st
import pickle
import pandas as pd
import requests

# Load the movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Fetch poster from API
import time

def fetch_poster(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey=90f86239"
    for attempt in range(3):  # Retry up to 3 times
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if data.get("Response") == "True":
                    poster_url = data.get('Poster', '')
                    if poster_url == 'N/A':  # Handle missing posters
                        return 'https://via.placeholder.com/300x450?text=No+Poster+Available'
                    return poster_url
                else:
                    print(f"OMDb Error: {data.get('Error')} for {movie_title}")
                    return 'https://via.placeholder.com/300x450?text=No+Poster+Available'
            else:
                print(f"Error: Status code {response.status_code} for {movie_title}")
        except requests.JSONDecodeError:
            print(f"Error: Failed to decode JSON for {movie_title}. Retrying...")
        time.sleep(1)  # Wait 1 second before retrying
    return 'https://via.placeholder.com/300x450?text=No+Poster+Available'


 # Correct the key to 'Poster'

def recommend(movie):
    # Get the movie index based on the title
    movie_index = movies[movies['title'] == movie].index[0]
    
    # Get the similarity scores for the selected movie
    distances = similarity[movie_index]
    
    # Get the top 5 recommended movies (excluding the movie itself)
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommend_movies_posters = []
    
    # Loop through the recommended movies to fetch their details
    for i in movies_list:
        movie_title = movies.iloc[i[0]].title  # Get movie title for the recommended movie
        recommended_movies.append(movie_title)  # Append the movie title
        recommend_movies_posters.append(fetch_poster(movie_title))  # Append the poster URL

    return recommended_movies, recommend_movies_posters


# Streamlit interface
st.title('Movie Recommendation System')

# Dropdown for selecting a movie
select_movie_name = st.selectbox('Select a movie', movies['title'].values)

if st.button('Recommend'):
    # Get recommended movies and posters
    names, posters = recommend(select_movie_name)

    # Display the recommended movies and posters
    cols = st.columns(5)  # Create 5 columns for displaying the recommended movies
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])

# Optionally, display the recommended movie titles in a list format
    st.write("Recommended Movies:")
    for name in names:
        st.write(name)