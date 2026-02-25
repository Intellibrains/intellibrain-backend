"""
Authentication Utility Functions

This file handles all security-related operations:

- Password hashing using Argon2 via pwdlib
- Password verification during login
- JWT token creation for user sessions

JWT tokens include an expiration time to ensure secure authentication.

This module is designed to be reusable and will work with
database integration in later stages.

Author: Ankit Kalyani
"""
from datetime import datetime, timedelta
from jose import jwt
from pwdlib import PasswordHash

SECRET_KEY = "mysecretkey123"
ALGORITHM = "HS256"

pwd_hash = PasswordHash.recommended()

def hash_password(password: str):
    return pwd_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=60)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)