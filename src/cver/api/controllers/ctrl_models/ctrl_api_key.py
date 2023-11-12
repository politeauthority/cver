"""
    Cver Api - Controller Model
    Api Key

"""
import logging

from flask import Blueprint, jsonify, Response, make_response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.api_key import ApiKey
from cver.api.utils import auth
from cver.api.utils import api_util

ctrl_api_key = Blueprint("api-key", __name__, url_prefix="/api-key")


@ctrl_api_key.route("")
@ctrl_api_key.route("/")
@ctrl_api_key.route("/<api_key_id>")
@auth.auth_request
def get_model(api_key_id: int = None) -> Response:
    """GET operation for a ApiKey.
    GET /api-key
    """
    data = ctrl_base.get_model(ApiKey, api_key_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_api_key.route("", methods=["POST"])
@ctrl_api_key.route("/", methods=["POST"])
@ctrl_api_key.route("/<api_key_id>", methods=["POST"])
@auth.auth_request
def post_model(api_key_id: int = None):
    """POST operation for a ApiKey model. We need to generate a client_id and api_key for the user
    before saving. On the response back to the client, send the plaintext api key, this is the only
    time we'll share the api key.
    POST /api-key
    """
    logging.info("Creating ApiKey for")
    plaintext_api_key = auth.generate_api_key()
    args = api_util.get_params()
    if "user_id" not in args["raw_args"]:
        data = {
            "status": "Error",
            "message": "A user_id must be given to create an api key"
        }
        return make_response(jsonify(data), 400)

    api_key_details = {
        "user_id": args["raw_args"]["user_id"],
        "client_id": auth.generate_client_id(),
        "key": auth.generate_hash(plaintext_api_key),
        "expiration_date": None
    }
    data, response = ctrl_base.post_model(ApiKey, api_key_id, api_key_details)
    data["object"]["key"] = plaintext_api_key
    return jsonify(data), 201


@ctrl_api_key.route("/<api_key_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(api_key_id: int = None):
    """DELETE operation for a ApiKey entity.
    DELETE /api-key
    """
    logging.debug("DELETE ApiKey")
    return ctrl_base.delete_model(ApiKey, api_key_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_api_key.py
