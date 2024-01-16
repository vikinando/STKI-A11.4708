# functions.py

# Importing necessary libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def load_and_preprocess_data(file_path):
    """
    Loads and preprocesses the anime data.
    """
    df = pd.read_csv(file_path)
    df.dropna(inplace=True)
    df.drop("Score", axis=1, inplace=True)
    return df

def create_tfidf_matrix(df):
    """
    Creates a TF-IDF matrix from the anime synopsis.
    """
    vectorizer = TfidfVectorizer(stop_words="english", analyzer="word")
    tfidf_matrix = vectorizer.fit_transform(df["sypnopsis"])
    return tfidf_matrix

def create_cosine_similarity_matrix(tfidf_matrix):
    """
    Creates a cosine similarity matrix from the TF-IDF matrix.
    """
    cos_sim = cosine_similarity(tfidf_matrix)
    return cos_sim

def recommend_animes(df, cos_sim, anime_name, rec_count=5):
    """
    Recommends animes based on a given anime name.
    """
    indices = pd.Series(df.index, index=df["Name"])
    indices = indices[~indices.index.duplicated(keep="last")]
    
    if anime_name not in indices:
        return ["Anime not found."]
    
    anime_index = indices[anime_name]
    similarity_score = pd.DataFrame(cos_sim[anime_index], columns=["score"])
    similar_animes = similarity_score.sort_values(by="score", ascending=False)\
                                     .iloc[1:rec_count+1].index
    return df["Name"].iloc[similar_animes].tolist()

def master_recommendation_function(anime_name, rec_count=5, file_path="anime_with_synopsis.csv"):
    """
    Master function to handle the recommendation process.
    """
    df = load_and_preprocess_data(file_path)
    tfidf_matrix = create_tfidf_matrix(df)
    cos_sim = create_cosine_similarity_matrix(tfidf_matrix)
    return recommend_animes(df, cos_sim, anime_name, rec_count)
