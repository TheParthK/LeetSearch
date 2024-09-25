import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
df = pd.read_csv('leetcode_problems.csv')

# Initialize models
@st.cache(allow_output_mutation=True)
def load_sbert_model():
    return SentenceTransformer('paraphrase-MiniLM-L6-v2')

@st.cache
def load_tfidf_vectorizer():
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['description'])
    return vectorizer, tfidf_matrix

# Load precomputed SBERT embeddings
@st.cache(allow_output_mutation=True)
def load_sbert_embeddings():
    try:
        return np.load('description_embeddings.npy')
    except FileNotFoundError:
        model = load_sbert_model()
        embeddings = model.encode(df['description'].tolist(), show_progress_bar=True)
        np.save('description_embeddings.npy', embeddings)
        return embeddings

# Function to find similar problems using SBERT
def find_similar_problems_sbert(user_query, top_n=7):
    model = load_sbert_model()
    description_embeddings = load_sbert_embeddings()
    query_embedding = model.encode([user_query])
    cosine_sim = cosine_similarity(query_embedding, description_embeddings).flatten()
    similar_indices = cosine_sim.argsort()[-top_n:][::-1]
    return df.iloc[similar_indices][['title', 'url', 'difficulty', 'acceptance_rate']]

# Function to find similar problems using TF-IDF
def find_similar_problems_tfidf(user_query, top_n=7):
    vectorizer, tfidf_matrix = load_tfidf_vectorizer()
    query_vec = vectorizer.transform([user_query])
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    similar_indices = cosine_sim.argsort()[-top_n:][::-1]
    return df.iloc[similar_indices][['title', 'url', 'difficulty', 'acceptance_rate']]

# Streamlit app interface
st.title('LeetCode Problem Similarity Finder')
st.write("Enter a problem description to find similar LeetCode problems.")

# User input
user_query = st.text_input("Problem Description", "Find the longest substring without repeating characters")

# Choose method

word_embeddings_method_title = "Word Embeddings (SBERT) - Takes Longer - Only works locally"
tf_idf_method_title = "TF-IDF"

method = st.radio("Choose a method:", (tf_idf_method_title, word_embeddings_method_title))


def display_table(similar_problems):
    # Create a new dataframe with the necessary columns
    table_data = pd.DataFrame({
        # 'S.No.': range(1, len(similar_problems) + 1),  # Generate serial numbers starting from 1
        'Title': similar_problems['title'],
        'Difficulty': similar_problems['difficulty'],
        'Link': similar_problems['url'].apply(lambda x: f'<a href="{x}" target="_blank">Link</a>')
    })
    
    # Apply styling to center both the headers (th) and the rows (td)
    styled_table = table_data.style.set_properties(**{'text-align': 'center'}) \
                                  .set_table_styles([{
                                      'selector': 'th',
                                      'props': [('text-align', 'center')]
                                  }, {
                                      'selector': 'td',
                                      'props': [('text-align', 'center')]  # This centers the row content
                                  }])
    
    # Display the table using Streamlit's st.write with HTML rendering
    st.write(styled_table.to_html(escape=False), unsafe_allow_html=True)

# Example usage in your app
# similar_problems = find_similar_problems(user_query)  # This is a placeholder, based on your code.
# display_table(similar_problems)
# Display results
if st.button("Find Similar Problems"):
    if method == word_embeddings_method_title:
        st.write("Using Word Embeddings (SBERT):")
        similar_problems = find_similar_problems_sbert(user_query)
    else:
        st.write("Using TF-IDF:")
        similar_problems = find_similar_problems_tfidf(user_query)
    display_table(similar_problems)
    # Display similar problems
    # i = 0
    # for idx, row in similar_problems.iterrows():
    #     st.write(f"{i + 1}. **{row['title']}** (Difficulty: {row['difficulty']}, Acceptance Rate: {row['acceptance_rate']}%)")
    #     st.write(f"[Problem Link]({row['url']})")
    #     i += 1
