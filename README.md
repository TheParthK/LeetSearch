LeetSearch
===============================
> <**The LeetCode Problem Similarity Website API**\>

Try it! ->
**_[LeetSearch Streamlit App](https://leetsearch.streamlit.app)_**



This project is an NLP-powered FastAPI-based API that allows users to find similar LeetCode problems based on a query or problem description. It uses two methods for similarity calculation: **TF-IDF** and **word embeddings (Sentence-BERT)**. The project is deployed and accessible via Streamlit and API endpoints.

Features
--------

*   **Two similarity methods**: Choose between TF-IDF and word embeddings (Sentence-BERT).
*   **Real-time problem matching**: Finds the most similar problems from a dataset of 1,825 LeetCode problems.
*   **Deployed on Heroku (or other cloud services)**: Provides real-time access for concurrent users.

Dataset
-------

The dataset consists of **1,825 LeetCode problems** and contains the following columns:

*   **id**: Problem identifier
*   **title**: Problem title
*   **description**: Problem description
*   **is\_premium**: Premium status
*   **difficulty**: Problem difficulty (easy, medium, hard)
*   **solution\_link**: Link to the solution
*   **acceptance\_rate**: Problem acceptance rate
*   **frequency**: How often the problem is asked
*   **url**: LeetCode problem link
*   **discuss\_count**: Number of discussions related to the problem

Tech Stack
----------

*   **Backend**: FastAPI
*   **Frontend**: Streamlit (optional)
*   **Machine Learning**: TF-IDF, Sentence-BERT (using SentenceTransformers)
*   **Deployment**: Heroku or Vercel

How It Works
------------

1.  **TF-IDF Method**: Converts problem descriptions into a TF-IDF matrix and computes cosine similarity between the query and problem descriptions.
2.  **Word Embeddings (Sentence-BERT)**: Encodes problem descriptions and the user query into sentence embeddings (768 dimensions), then calculates cosine similarity.

Installation
------------

### Prerequisites

*   Python 3.8+
*   FastAPI
*   Uvicorn (for running the FastAPI server)
*   Vercel or Heroku CLI (for deployment)

### Install Dependencies

1.  Clone the repository:
    
    ```bash
    git clone https://github.com/yourusername/leetcode-similarity-api.git
    cd leetcode-similarity-api
    ```
    
2.  Install required Python packages:
    
    ```bash
    pip install -r requirements.txt
    ```
    

### Dataset

Make sure the `leetcode_problems.csv` dataset is located in the root directory of your project.

Running the Project
-------------------

### Local Development

1.  Run the FastAPI app locally using Uvicorn:
    
    ```bash
    uvicorn api:app --reload
    ```
    
2.  Access the API documentation at:
    
    ```
    http://127.0.0.1:8000/docs
    ```
    
3.  Try the `/get_similar_problems/` endpoint to get similar LeetCode problems based on a query.
    

### Streamlit Frontend

To run the Streamlit app:

```bash
streamlit run app.py
```

Deployment
----------

### Heroku Deployment

1.  Create a `Procfile`:
    
    ```
    web: uvicorn api:app --host 0.0.0.0 --port $PORT
    ```
    
2.  Log in to Heroku:
    
    ```bash
    heroku login
    ```
    
3.  Create a new Heroku app and deploy:
    
    ```bash
    heroku create
    git push heroku master
    ```
    

### Vercel Deployment

1.  Add `vercel.json` in the root of your project:
    
    ```json
    
    {
      "version"
    : 2
    ,
      "builds"
    : [
        { "src"
    : "api/api.py"
    , "use"
    : "@vercel/python" }
      ]
    ,
      "routes"
    : [
        { "src"
    : "/(.*)"
    , "dest"
    : "api/api.py" }
      ]
    }
    ```
    
2.  Deploy using Vercel CLI:
    
    ```bash
    vercel --prod
    ```
    

API Endpoints
-------------

### `/get_similar_problems/`

*   **Method**: `POST`
    
*   **Description**: Returns a list of similar LeetCode problems based on a query description.
    
*   **Request Body**:
    
    ```json
    
    {
      "query"
    : "Given an array of integers, find the largest sum of a contiguous subarray."
    ,
      "method"
    : "tfidf"  // or "embeddings"
    }
    ```
    
*   **Response**:
    
    ```json
    
    [
      {
        "id"
    : 1
    ,
        "title"
    : "Maximum Subarray"
    ,
        "difficulty"
    : "Medium"
    ,
        "url"
    : "https://leetcode.com/problems/maximum-subarray/"
    ,
        "acceptance_rate"
    : "45.7%"
      }
    ,
      ...
    ]
    ```
    

Future Improvements
-------------------

*   Add support for more advanced embedding models (e.g., GPT, T5).
*   Implement caching mechanisms for frequently queried problems.
*   Enhance deployment scalability for concurrent user access.

License
-------

This project is licensed under the MIT License.

* * *

Feel free to customize this based on your preferences or additional features!

>Note: This is an auto-generated README file