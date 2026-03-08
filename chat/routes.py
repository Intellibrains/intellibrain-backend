import random
import string
import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .twilio_service import generate_twilio_token
from twilio.rest import Client

load_dotenv()

# Twilio Credentials
ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
API_KEY = os.getenv("TWILIO_API_KEY")
API_SECRET = os.getenv("TWILIO_API_SECRET")

twilio_client = Client(API_KEY, API_SECRET, ACCOUNT_SID)

router = APIRouter()

# --- Request Models for JSON Bodies ---

class CreateRoomRequest(BaseModel):
    username: str
    room_name: str

class JoinRoomRequest(BaseModel):
    room_code: str
    username: str

# --- Helpers ---

def generate_room_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# --- Endpoints ---

@router.get("/twilio-token/{username}")
def get_twilio_token(username: str):
    token = generate_twilio_token(username)
    return {"token": token}
    
@router.post("/create-room")
def create_room(data: CreateRoomRequest):
    room_code = generate_room_code()

    try:
        # 1. Create the conversation using the room_name as the 'friendly_name'
        conversation = twilio_client.conversations.v1.conversations.create(
            unique_name=room_code,
            friendly_name=data.room_name  # Save the creator's room name here
        )

        # 2. Add the creator
        twilio_client.conversations.v1.conversations(conversation.sid) \
            .participants.create(identity=data.username)

        return {"room_code": room_code, "room_name": data.room_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/join-room")
def join_room(data: JoinRoomRequest):
    try:
        # 1. Fetch the existing conversation to get the friendly_name
        conversation = twilio_client.conversations.v1.conversations(data.room_code).fetch()
        room_display_name = conversation.friendly_name

        # 2. Add the joining user
        twilio_client.conversations.v1.conversations(data.room_code) \
            .participants.create(identity=data.username)
        
        return {
            "message": "Room joined", 
            "room_code": data.room_code, 
            "room_name": room_display_name  # Send the original name back!
        }
    except Exception as e:
        # If already joined, we still want to fetch the name to update the UI
        try:
            conversation = twilio_client.conversations.v1.conversations(data.room_code).fetch()
            return {
                "message": "Already joined", 
                "room_code": data.room_code, 
                "room_name": conversation.friendly_name
            }
        except:
            raise HTTPException(status_code=404, detail="Room not found")