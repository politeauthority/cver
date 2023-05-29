"""Auth Utilities

"""
import datetime
from functools import wraps
import logging
import random

from flask import make_response, request, jsonify
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from werkzeug import security

from cver.api.models.api_key import ApiKey
from cver.api.utils import glow

SECRET_KEY = "my-secret-key"


def auth_request(f):
    """Authentication decorator, which gates HTTP routes. This method used to validate user access
    via a JWT.
    """
    @wraps(f)
    def decorator(*args, **kwargs):
        data = {
            "message": "",
            "status": "Error"
        }
        if "Token" not in request.headers:
            data["message"] = "Missing token"
            return make_response(jsonify(data), 401)
        token = request.headers["Token"]
        jwt_value = validate_jwt(token)
        if jwt_value:
            logging.info("Authenticated User")
            print(jwt_value)
            return f(*args, **kwargs)
        else:
            logging.warning("Can't verify token")
            return make_response(jsonify({"message": "Invalid token"}), 401)
    return decorator


def verify_key(client_id: str, raw_api_key: str) -> bool:
    """"Authenticate a login request, taking the client_id and api_key looking for a match."""
    api_key = ApiKey()
    # Check for a matching Client ID
    if not api_key.get_by_client_id(client_id):
        logging.info("Could not find an ApiKey with client_id: %s" % client_id)
        return False

    # Check that the Api Key matches
    if security.check_password_hash(api_key.key, raw_api_key):
        logging.info("Authenticated client_id: %s" % client_id)
        return api_key.user_id
    else:
        logging.warning("Api key doesn't match client_id: %s" % client_id)
        return False


def validate_jwt(token) -> dict:
    """
    """
    try:
        # Decode and verify the JWT using the secret key
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except ExpiredSignatureError:
        # Handle expired token
        logging.warning("Token has expired.")
        return None
    except InvalidSignatureError:
        # Handle invalid signature
        logging.error("Invalid token signature.")
        return None


def mint_jwt(user_id: int):
    """Mint a JWT token for a User with the given expiration time.
    """
    expiration_minutes = glow.general["CVER_JWT_EXPIRE_MINUTES"]
    payload = {
        "user_id": user_id,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }

    # Create the JWT using the payload and secret key
    jwt_token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    return jwt_token


def generate_client_id():
    """Generates a client id to be used in api authentication."""
    length = 10
    characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    client_id = ""
    for index in range(length):
        client_id = client_id + random.choice(characters)
    return client_id


def generate_api_key():
    password_length = 19
    characters = "abcdefghijklmnopqrstuvwxyz1234567890"
    api_key = ""
    for index in range(password_length):
        api_key = api_key + random.choice(characters)
    api_key = "%s-%s-%s-%s" % (
        api_key[:4],
        api_key[5:9],
        api_key[10:14],
        api_key[15:])
    return api_key


def generate_hash(password: str) -> str:
    """Generate a password hash from a string"""
    return security.generate_password_hash(password, method="pbkdf2:sha256")


# End File: cver/src/api/utils/auth.py
