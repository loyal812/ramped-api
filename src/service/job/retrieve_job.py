import os
import difflib
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from src.core.db.mongodb.cl_mongodb import MongoDB
from pymongo import ASCENDING

# Load environment variables
load_dotenv()
mongodb_job_collection_name = os.getenv('MONGODB_JOB_COLLECTION_NAME')

def tokenize(sentence: str):
    return sentence.lower().split()

def perform_retrieve_job(job_name: str):
    # Initialize MongoDB connection
    db = MongoDB(collection_name=mongodb_job_collection_name)

    # Retrieve all job postings
    job_postings = list(db.collection.find({}, {'job_name': 1}))

    # Extract job names and tokenize them
    job_names = [job['job_name'] for job in job_postings]
    tokenized_job_names = {job['job_name']: tokenize(job['job_name']) for job in job_postings}

    # Tokenize the search parameter
    search_tokens = tokenize(job_name)
    
    # Perform fuzzy matching on tokens
    all_matches = set()
    for token in search_tokens:
        matches = difflib.get_close_matches(token, [token for tokens in tokenized_job_names.values() for token in tokens], n=10, cutoff=0.6)
        all_matches.update(matches)

    # Retrieve job postings for the matching tokens
    matching_job_names = {name for name, tokens in tokenized_job_names.items() if any(token in tokens for token in all_matches)}
    matching_jobs = db.collection.find({'job_name': {'$in': list(matching_job_names)}})

    # Convert matching jobs to a list and handle ObjectId
    job_list = []
    for job in matching_jobs:
        job['_id'] = str(job['_id'])  # Convert ObjectId to string
        job_list.append(job)

    # Encode the result with jsonable_encoder
    encoded_value = jsonable_encoder(job_list)

    return encoded_value