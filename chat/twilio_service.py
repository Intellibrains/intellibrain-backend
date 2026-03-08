
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

import os

ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
API_KEY = os.getenv("TWILIO_API_KEY")
API_SECRET = os.getenv("TWILIO_API_SECRET")
SERVICE_SID = os.getenv("TWILIO_SERVICE_SID")


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