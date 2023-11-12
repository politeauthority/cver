"""
    Cver Api - Controller Model
    Role

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.role import Role
from cver.api.utils import auth

ctrl_role = Blueprint("role", __name__, url_prefix="/role")


@ctrl_role.route("")
@ctrl_role.route("/")
@ctrl_role.route("/<role_id>")
@auth.auth_request
def get_model(role_id: int = None) -> Response:
    """GET operation for a Role.
    GET /role
    """
    role = ctrl_base.get_model(Role, role_id)
    if not isinstance(role, dict):
        return role
    return jsonify(role)


@ctrl_role.route("", methods=["POST"])
@ctrl_role.route("/", methods=["POST"])
@ctrl_role.route("/<role_id>", methods=["POST"])
@auth.auth_request
def post_model(role_id: int = None):
    """POST operation for a ROle model.
    POST /role
    """
    logging.info("POST Role")
    return ctrl_base.post_model(Role, role_id)


@ctrl_role.route("/<role_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(role_id: int = None):
    """DELETE operation for a Role model.
    DELETE /role
    """
    logging.debug("DELETE Role")
    return ctrl_base.delete_model(Role, role_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_role.py
