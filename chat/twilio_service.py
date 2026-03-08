
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
API_KEY = os.getenv("TWILIO_API_KEY")
API_SECRET = os.getenv("TWILIO_API_SECRET")
SERVICE_SID = os.getenv("TWILIO_SERVICE_SID")

if not ACCOUNT_SID or not API_KEY or not API_SECRET:
    raise RuntimeError("Twilio environment variables are missing")


def generate_twilio_token(username: str):

    token = AccessToken(
        ACCOUNT_SID,
        API_KEY,
        API_SECRET,
        identity=username
    )

    chat_grant = ChatGrant(service_sid=SERVICE_SID)
    token.add_grant(chat_grant)

    return token.to_jwt()