import pandas as  pd
movies=pd.read_csv(r'C:\Users\HP\OneDrive\Documents\movie\tmdb_5000_movies.csv')
credits=pd.read_csv(r'C:\Users\HP\OneDrive\Documents\creadit\tmdb_5000_credits.csv')


import ast
import pickle
import requests
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Merge data
movies = movies.merge(credits, on='title')

# Handle missing values
movies.dropna(inplace=True)

# Convert genres and keywords from string representation of lists to lists
def convert(obj):
    return [i['name'] for i in ast.literal_eval(obj)]

movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# Convert cast and crew
def convert_cast(obj):
    return [i['name'] for i in ast.literal_eval(obj)[:3]] if pd.notnull(obj) else []

def convert_crew(obj):
    return [i['name'] for i in ast.literal_eval(obj) if i['job'] == 'Director'][:1] if pd.notnull(obj) else []

movies['cast'] = movies['cast'].apply(convert_cast)
movies['crew'] = movies['crew'].apply(convert_crew)

# Process text fields
movies['overview'] = movies['overview'].fillna('').apply(lambda x: x.split())
movies['genres'] = movies['genres'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['keywords'] = movies['keywords'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['cast'] = movies['cast'].apply(lambda x: [i.replace(" ", "") for i in x])
movies['crew'] = movies['crew'].apply(lambda x: [i.replace(" ", "") for i in x])

# Combine tags
movies['tags'] = movies['genres'] + movies['keywords'] + movies['overview'] + movies['cast'] + movies['crew']
new_df = movies[['movie_id', 'title', 'tags']]
new_df.loc[:, 'tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Apply stemming
ps = PorterStemmer()

def stem(text):
    return " ".join([ps.stem(i) for i in text.split()])

new_df.loc[:, 'tags'] = new_df['tags'].apply(stem)

# Vectorization and similarity
cv = CountVectorizer(max_features=5000, stop_words='english')
vectors = cv.fit_transform(new_df['tags']).toarray()
similarity = cosine_similarity(vectors)

# Recommendation function
def normalize_title(title):
    return title.lower().replace("-", " ").strip()

# Update recommend function to fetch poster by title instead of movie_id
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


with open('movie_dict.pkl', 'wb') as movie_file:
    pickle.dump(new_df, movie_file)  # Save the dataframe directly

with open('similarity.pkl', 'wb') as similarity_file:
    pickle.dump(similarity, similarity_file)  # Save the similarity matrix directly