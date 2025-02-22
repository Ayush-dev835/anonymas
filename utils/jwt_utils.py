from configs_and_constants.env import env
import jwt
from datetime import datetime, timedelta

access_token_secret = env.get("access_token_secret")
refresh_token_secret = env.get("refresh_token_secret")


def generate_access_token(payload: dict):
    payload.update(
        {
            "exp": datetime.utcnow() + timedelta(hours=5),
            "iat": datetime.utcnow(),
        }
    )
    return jwt.encode(payload, access_token_secret, algorithm="HS256")


def generate_refresh_token(payload: dict):
    payload.update(
        {
            "exp": datetime.utcnow() + timedelta(minutes=30),
            "iat": datetime.utcnow(),
        }
    )
    return jwt.encode(payload, refresh_token_secret, algorithm="HS256")


def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, access_token_secret, algorithms=["HS256"])
        return None, payload
    except Exception as error:
        return str(error), None
