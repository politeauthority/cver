"""
    Cver Api - Controller
    Index

"""
import logging

from flask import Blueprint, jsonify, request

from cver.api.stats import totals
from cver.api.stats import tasks as tasks_stats
from cver.api.utils import auth
from cver.api.utils import glow
from cver.api.models.user import User
from cver.migrate.migrate import CURRENT_MIGRATION

ctrl_index = Blueprint("index", __name__, url_prefix="/")


@ctrl_index.route("/")
def index():
    logging.info("Serving /")
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"],
        "build_short": glow.general["CVER_BUILD_SHORT"],
    }
    return jsonify(data)


@ctrl_index.route("/auth", methods=["POST"])
def authenticate():
    logging.debug("Starting authentication flow")
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
    api_key_raw = request.headers["X-Api-Key"]
    authed_event = auth.verify_api_key(client_id, api_key_raw)
    if not authed_event:
        logging.warning("Failed login attempt, client_id: %s" % client_id)
        return jsonify(data), 403
    logging.info("Verified api key")

    user = User()
    user.get_by_id(authed_event["user_id"])
    glow.user["user_id"] = user.id
    glow.user["org_id"] = user.org_id
    glow.user["role_id"] = user.role_id
    auth.record_last_access(user, authed_event["api_key"])

    # Mint the JWT
    data["token"] = auth.mint_jwt()
    data["message"] = "Authenticated user and minted token"
    data["status"] = "Success"
    logging.info("Sending back the token to the client")
    return jsonify(data)


@ctrl_index.route("/info")
@auth.auth_request
def info():
    model_totals = totals.get_model_totals()
    task_totals = tasks_stats.get_task_totals()
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"],
        "build_short": glow.general["CVER_BUILD_SHORT"],
        "migration": CURRENT_MIGRATION,
        "tasks": task_totals,
        "model_totals": model_totals,
        "deployed_at": glow.general["CVER_DEPLOYED_AT"]
    }
    return jsonify(data)


@ctrl_index.route("/healthz")
def healthz():
    data = {
        "status": "Success",
        "message": "Healthy"
    }
    if glow.general["CVER_LOG_HEALTH_CHECKS"]:
        logging.info("Helath check, reporting healthy")
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
