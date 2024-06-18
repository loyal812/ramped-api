import os
from dotenv import load_dotenv
from src.core.db.mongodb.cl_mongodb import MongoDB

from datetime import datetime, timedelta
from passlib.context import CryptContext
import jwt
from typing import Tuple

# Load environment variables
load_dotenv()
mongodb_user_collection_name = os.getenv('MONGODB_USER_COLLECTION_NAME')
jwt_secret = os.getenv('JWT_SECRET_KEY')
jwt_algorithm = 'HS256'

# Create a CryptContext object
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def perform_signup(email: str, password: str, password2: str):
    if password != password2:
        return {"error": "Passwords do not match"}
    
    password_valid, validation_message = is_valid_password(password)
    if not password_valid:
        return {"error": validation_message}
    
    db = MongoDB(collection_name=mongodb_user_collection_name)
    
    if db.collection.find_one({"email": email}):
        return {"error": "User already exists"}
    
    hashed_password = pwd_context.hash(password)
    user_data = {
        "email": email,
        "password": hashed_password,
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    try:
        db.collection.insert_one(user_data)
        token = generate_token(email)
        return {"message": "Signup successful", "token": token}
    except Exception as e:
        return {"error": str(e)}

def is_valid_password(password: str) -> Tuple[bool, str]:
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter"
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one capital letter"
    if not any(char in "!@#$%^&*()-_+=<>?{}[]|\/" for char in password):
        return False, "Password must contain at least one special character"
    return True, "Password is valid"

def generate_token(email: str) -> str:
    payload = {
        "email": email,
        "exp": datetime.now() + timedelta(hours=24)  # Token expires in 24 hours
    }
    return jwt.encode(payload, jwt_secret, algorithm=jwt_algorithm)

def perform_signin(email: str, password: str):
    return