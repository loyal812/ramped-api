# Ramped Job Portal Backend API

This repository contains the backend API for a job portal site, developed using Python, FastAPI, and MongoDB. The API includes endpoints for user signup, signin, and retrieving jobs with fuzzy matching using the `difflib` library.  

## Features

- User Signup
- User Signin
- Retrieve Jobs with Fuzzy Matching Algorithm

## Getting Started

### Prerequisites

- Python 3.8+
- MongoDB

### Installation

1. Clone the repository:

```bash
git clone https://github.com/loyal812/ramped-api.git
cd ramped-api
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Install the dependencies:

```bash
pip install -r requirements-linux.txt  # On Windows use `pip install -r requirements-windows.txt`
```

4. Set up your MongoDB connection and JWT Secert Key in the `.env` file:

```env
MONGODB_USERNAME=
MONGODB_PASSWORD=
MONGODB_CLUSTER_NAME=
MONGODB_DATABASE_NAME=
MONGODB_JOB_COLLECTION_NAME=
MONGODB_USER_COLLECTION_NAME=
JWT_SECRET_KEY=
```

### Running the Application

1. Start the FastAPI server:

```bash
py .\src\main.py
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoints

### Signup

- **URL:** `/api/v1/auth/signup`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "email",
    "password": "password",
    "password2": "confirm password"
  }
  ```
- **Response:**
  1) Success
    ```json
    {
        "message": "Signup successful", 
        "token": "token"
    }
    ```
  2) Failed
    ```json
    {"error": "Passwords do not match"}
    {"error": "User already exists"}
    {"error": "Password must be at least 8 characters long"}
    {"error": "Password must contain at least one digit"}
    {"error": "Password must contain at least one letter"}
    {"error": "Password must contain at least one capital letter"}
    {"error": "Password must contain at least one special character"}
    ```

### Signin

- **URL:** `/api/v1/auth/signin`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "email": "email",
    "password": "password"
  }
  ```
- **Response:**
  1) Success
    ```json
    {
        "message": "Signin successful", 
        "token": "token"
    }
    ```
  2) Failed
    ```json
    {"error": "User does not exist"}
    {"error": "Invalid password"}
    ```

### Retrieve Jobs with Fuzzy Matching

- **URL:** `/api/v1/job/retrieve_job`
- **Method:** `POST`
- **Request Body:**
  ```json
  {
    "job_name": "retrieve job string",
  }
  ```
- **Response:**
  ```json
  [
    {
      "_id": "1",
      "job_name": "Software Developer",
      "job_full_text": "Job description ...",
      ...
    },
    ...
  ]
  ```

## Expanding the Implementation

### Semantic Matching

To expand this implementation to include semantic matches, such as matching "software engineer" to "developer", we can use a more advanced natural language processing (NLP) approach. Here are some suggestions:

1. **Using Word Embeddings:**
   - Use pre-trained word embeddings (e.g., Word2Vec, GloVe) to represent job titles and queries as vectors. Compute the cosine similarity between vectors to find semantically similar jobs.

2. **Using Transformers:**
   - Implement a model like BERT to capture contextual relationships between words. Fine-tune a pre-trained BERT model on your job dataset to improve matching accuracy.

3. **Implementing a Semantic Search Engine:**
   - Use Elasticsearch with a plugin like `elasticsearch-dsl` to index job titles and descriptions. Utilize its full-text search capabilities with semantic query enhancements.
