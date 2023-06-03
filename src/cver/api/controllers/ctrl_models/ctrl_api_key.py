"""
    Cver Api - Controller Model
    Api Key

"""
from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.api_key import ApiKey
from cver.api.utils import auth

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


# @ctrl_api_key.route("", methods=["POST"])
# @ctrl_api_key.route("/", methods=["POST"])
# @ctrl_api_key.route("/<api_key_id>", methods=["POST"])
# @auth.auth_request
# def post_model(api_key_id: int = None):
#     """POST operation for a ApiKey model.
#     POST /api-key
#     """
#     logging.info("POST ApiKey")
#     return ctrl_base.post_model(ApiKey, api_key_id)


# @ctrl_api_key.route("/<api_key_id>", methods=["DELETE"])
# @auth.auth_request
# def delete_model(api_key_id: int = None):
#     """DELETE operation for a ImageBuild model.
#     DELETE /api-key
#     """
#     logging.debug("DELETE ImageBuild")
#     return ctrl_base.delete_model(ApiKey, api_key_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_api_key.py
