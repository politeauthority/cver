"""
    Cver Api - Controller
    Index

"""
import logging

from flask import Blueprint, jsonify, request

from cver.api.models.user import User
from cver.api.utils import auth
from cver.api.utils import date_utils
from cver.api.utils import glow

ctrl_index = Blueprint("index", __name__, url_prefix="/")


@ctrl_index.route("/")
def index():
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    return jsonify(data)


@ctrl_index.route("/auth", methods=["POST"])
def auth_request():
    data = {
        "message": "Failed login",
        "status": "Error"
    }
    if "X-Api-Key" not in request.headers or "Client-Id" not in request.headers:
        data["message"] = "No api key sent with request."
        logging.warning("No api key sent with request.")
        return jsonify(data), 400

    # Try to authenticate
    client_id = request.headers["Client-Id"]
    api_key = request.headers["X-Api-Key"]
    verified_key = auth.verify_key(client_id, api_key)
    if not verified_key:
        logging.warning("Failed login attempt")
        return jsonify(data), 403
    user_id = verified_key

    # Update the User
    user = User()
    user.get_by_id(user_id)
    user.last_login = date_utils.now()
    user.save()

    # Mint the JWT
    data["token"] = auth.mint_jwt(user_id)
    data["message"] = "Authenticated and minted token"
    data["status"] = "Success"
    return jsonify(data)


@ctrl_index.route("/info")
@auth.auth_request
def info():
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    return jsonify(data)


# End File: cve/src/api/controllers/ctrl_index.py
