from fastapi import FastAPI, Query
from pydantic import BaseModel
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('leetcode_problems.csv')

# Initialize FastAPI app
app = FastAPI()

# Load the pre-trained Sentence-BERT model
embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(df['description'].tolist())

# Compute Sentence-BERT embeddings (word embeddings method)
description_embeddings = embedding_model.encode(df['description'].tolist(), show_progress_bar=True)


# Request schema
class QueryRequest(BaseModel):
    user_query: str
    method: str  # "tfidf" or "embeddings"
    top_k: int = 5


# Define the FastAPI endpoint
@app.post("/get_similar_problems/")
def get_similar_problems(query: QueryRequest):
    user_query = query.user_query
    method = query.method.lower()
    top_k = query.top_k

    if method == "tfidf":
        # TF-IDF Method
        query_vector = tfidf_vectorizer.transform([user_query])
        similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    elif method == "embeddings":
        # Word Embeddings Method (Sentence-BERT)
        query_embedding = embedding_model.encode([user_query])
        similarities = cosine_similarity(query_embedding, description_embeddings).flatten()
    else:
        return {"error": "Invalid method. Choose either 'tfidf' or 'embeddings'."}

    # Get top_k most similar problems
    top_indices = similarities.argsort()[-top_k:][::-1]
    similar_problems = df.iloc[top_indices]

    # Prepare the response
    response = []
    for _, row in similar_problems.iterrows():
        problem_data = {
            "S.No.": row['id'],
            "Title": row['title'],
            "Difficulty": row['difficulty'],
            "Link": row['url']
        }
        response.append(problem_data)

    return response