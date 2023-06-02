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
    logging.info("Serving /")
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    return jsonify(data)


@ctrl_index.route("/auth", methods=["POST"])
def authenticate():
    logging.info("Starting authentication flow")
    data = {
        "message": "Failed login",
        "status": "Error"
    }
    if "X-Api-Key" not in request.headers or "Client-Id" not in request.headers:
        if not "X-Api-Key" not in request.headers:
            data["message"] = "No api key sent with request."
            logging.warning("No api key sent with request")
        elif "Client-Id" not in request.headers:
            data["message"] = "No client id sent with request"
            logging.warning("No client id sent with request")
        return jsonify(data), 400

    # Try to authenticate
    client_id = request.headers["Client-Id"]
    api_key = request.headers["X-Api-Key"]
    verified_key = auth.verify_key(client_id, api_key)
    if not verified_key:
        logging.warning("Failed login attempt")
        return jsonify(data), 403
    logging.info("Verified api key")
    user_id = verified_key

    logging.info("User ID: %s" % user_id)
    # Update the User
    user = User()
    user.get_by_id(user_id)
    user.last_access = date_utils.now()
    logging.info("Updating user last access.")
    user.save()

    logging.info("Updated %s" % user)
    # Mint the JWT
    data["token"] = auth.mint_jwt(user_id)
    data["message"] = "Authenticated user and minted token"
    data["status"] = "Success"
    logging.info("Sending back the token to the client")
    return jsonify(data)


@ctrl_index.route("/info")
@auth.auth_request
def info():
    logging.info("Begin Info Request")
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    logging.info("Get ready to send data to client.")
    return jsonify(data)


@ctrl_index.route("/debug")
def debug():
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    if glow.general["CVER_TEST"]:
        data["test"] = True
    return jsonify(data)


# End File: cve/src/api/controllers/ctrl_index.py
