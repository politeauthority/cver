"""
    Cver Api - Controller Model
    RolePerm

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.role_perm import RolePerm
from cver.api.utils import auth

ctrl_role_perm = Blueprint("role-perm", __name__, url_prefix="/role-perm")


@ctrl_role_perm.route("")
@ctrl_role_perm.route("/")
@ctrl_role_perm.route("/<role_perm_id>")
@auth.auth_request
def get_model(role_perm_id: int = None) -> Response:
    """GET operation for a Role.
    GET /role-perm
    """
    role = ctrl_base.get_model(RolePerm, role_perm_id)
    if not isinstance(role, dict):
        return role
    return jsonify(role)


@ctrl_role_perm.route("", methods=["POST"])
@ctrl_role_perm.route("/", methods=["POST"])
@ctrl_role_perm.route("/<role_perm_id>", methods=["POST"])
@auth.auth_request
def post_model(role_perm_id: int = None):
    """POST operation for a ROle model.
    POST /role-perm
    """
    logging.info("POST RolePerm")
    return ctrl_base.post_model(RolePerm, role_perm_id)


@ctrl_role_perm.route("/<role_perm_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(role_perm_id: int = None):
    """DELETE operation for a Image model.
    DELETE /role-perm
    """
    logging.debug("DELETE RolePerm")
    return ctrl_base.delete_model(RolePerm, role_perm_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_role_perm.py
