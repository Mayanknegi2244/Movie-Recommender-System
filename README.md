# Movie-Recommender-System
This is a content-based movie recommendation system built using Python, Pandas, Scikit-Learn, and Streamlit. It recommends similar movies based on genres, cast, crew, keywords, and overview using cosine similarity on vectorized tags. The system also fetches movie posters via the OMDb API for better visualization.

🚀 Features

✅ Content-based recommendations using cosine similarity

✅ Data preprocessing (genres, cast, crew, keywords, overview)

✅ Stemming using PorterStemmer

✅ Poster fetching via OMDb API

✅ Interactive Streamlit Web App

✅ Saves processed data with Pickle (movie_dict.pkl & similarity.pkl)

📂 Project Structure
Movie-Recommendation-System/
│
├── tmdb_5000_movies.csv          # Movies dataset
├── tmdb_5000_credits.csv         # Credits dataset
├── app.py                        # Streamlit app
├── model.py                      # Preprocessing + Model building
├── movie_dict.pkl                # Pickled dataframe
├── similarity.pkl                # Pickled similarity matrix
├── README.md                     # Project documentation

⚙️ Installation

Clone the repository

git clone https://github.com/your-username/Movie-Recommendation-System.git
cd Movie-Recommendation-System


Install dependencies

pip install -r requirements.txt


requirements.txt should include:

pandas
numpy
scikit-learn
nltk
streamlit
requests


Download datasets

TMDB 5000 Movies Dataset

Place tmdb_5000_movies.csv and tmdb_5000_credits.csv in the project folder.

▶️ Usage
Step 1: Build Model & Save Files

Run the preprocessing + model script (model.py):

python model.py


This will generate movie_dict.pkl and similarity.pkl.

Step 2: Run Streamlit App
streamlit run app.py

Step 3: Explore Recommendations 🎥

Select a movie from the dropdown.

Click Recommend.

Get top 5 similar movies with posters.

🖼️ Example Output

Input: Avatar
Recommendations:

John Carter

Guardians of the Galaxy

Star Trek

Star Wars: The Force Awakens

The Last Airbender

🔑 API Key Setup

This project uses the OMDb API for fetching posters.
.

Replace apikey=90f86239 in the code with your key.

📌 Future Improvements

Improve recommendation accuracy with TF-IDF or Deep Learning embeddings

Add collaborative filtering for hybrid recommendations

Deploy to Streamlit Cloud / Heroku / AWS



Dataset: Kaggle - TMDB Movie Metadata

API: OMDb API
