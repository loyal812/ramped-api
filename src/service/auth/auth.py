import os
from dotenv import load_dotenv
from src.core.db.mongodb.cl_mongodb import MongoDB

from datetime import datetime

load_dotenv()
mongodb_collection_name = os.getenv('MONGODB_COLLECTION_NAME')

def perform_signup():
    return

def perform_signin():
    return