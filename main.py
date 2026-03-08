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
from fastapi.middleware.cors import CORSMiddleware
from chat.routes import router as chat_router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.include_router(chat_router, prefix="/chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)

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

    token = create_access_token({"sub": user.email})

    return {
        "user": {
            "id": user.email,   # using email as temp ID
            "name": user.full_name,
            "email": user.email,
            "plan": "free"
        },
        "token": token
    }

@app.post("/signin")
def signin(user: SigninUser):
    if user.email not in fake_db:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    stored_user = fake_db[user.email]

    if not verify_password(user.password, stored_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.email})

    return {
    "user": {
        "id": user.email,
        "name": stored_user["full_name"],
        "email": user.email,
        "plan": "free"
    },
    "token": token

    }

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_react(full_path: str):
    file_path = os.path.join(DIST_DIR, full_path)

    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)

    return FileResponse(os.path.join(DIST_DIR, "index.html"))




  

    
 