# NOTE:
# Using in-memory fake_db for development testing.
# To be replaced with real database integration later.
"""
Authentication API Service (FastAPI)

This file contains the main backend logic for user authentication.

Features implemented:
- User Signup API (/signup)
- User Signin API (/signin)
- Password hashing using pwdlib (Argon2 algorithm)
- JWT token generation for secure login sessions
- Temporary in-memory database (fake_db) used for development/testing

NOTE:
fake_db is used only for local development and will be replaced
with a real database (PostgreSQL) in production.

Author: Ankit Kalyani
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from auth import hash_password, verify_password, create_access_token

app = FastAPI()

# Temporary database (for testing)
fake_db = {}

class SignupUser(BaseModel):
    full_name: str
    email: str
    password: str

class SigninUser(BaseModel):
    email: str
    password: str

@app.post("/signup")
def signup(user: SignupUser):
    if user.email in fake_db:
        raise HTTPException(status_code=400, detail="User already exists")

    fake_db[user.email] = {
        "full_name": user.full_name,
        "password": hash_password(user.password)
    }

    return {"message": "User created successfully"}

@app.post("/signin")
def signin(user: SigninUser):
    if user.email not in fake_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    stored_user = fake_db[user.email]

    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
        "access_token": token,
        "full_name": stored_user["full_name"],
        "email": user.email
    }
    
 