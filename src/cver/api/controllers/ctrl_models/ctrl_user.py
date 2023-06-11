"""
    Cver Api - Controller Model
    User

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.user import User
from cver.api.utils import auth

ctrl_user = Blueprint("user", __name__, url_prefix="/user")


@ctrl_user.route("")
@ctrl_user.route("/")
@ctrl_user.route("/<user_id>", methods=["GET"])
@auth.auth_request
def get_model(user_id: int = None) -> Response:
    """GET operation for a User.
    GET /user
    """
    logging.info("GET - /user")
    data = ctrl_base.get_model(User, user_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_user.route("", methods=["POST"])
@ctrl_user.route("/", methods=["POST"])
@ctrl_user.route("/<user_id>", methods=["POST"])
@auth.auth_request
def post_model(user_id: int = None):
    """POST operation for a User model.
    POST /role
    """
    logging.info("POST User")
    return ctrl_base.post_model(User, user_id)


@ctrl_user.route("/<user_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(user_id: int = None):
    """DELETE operation for a User model.
    DELETE /user
    """
    logging.debug("DELETE User")
    return ctrl_base.delete_model(User, user_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_user.py
