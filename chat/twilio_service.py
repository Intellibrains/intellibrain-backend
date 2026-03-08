
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant

ACCOUNT_SID = "AC1c5c3e959d710b360207f7d73923f6a4"
API_KEY = "SK714412d49612dfaed96ccf781b4c1417"
API_SECRET = "uMm2A71bkHHWrwNem4j0T9QqmRxpysMp"
SERVICE_SID = "IS6cfae4dcfccc468a850acd39ef86ac66"


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