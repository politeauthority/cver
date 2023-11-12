"""
    Cver Api - Controller Model
    Perm

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.perm import Perm
from cver.api.utils import auth

ctrl_perm = Blueprint("perm", __name__, url_prefix="/perm")


@ctrl_perm.route("")
@ctrl_perm.route("/")
@ctrl_perm.route("/<perm_id>")
@auth.auth_request
def get_model(perm_id: int = None) -> Response:
    """GET operation for a Perm.
    GET /perm
    """
    role = ctrl_base.get_model(Perm, perm_id)
    if not isinstance(role, dict):
        return role
    return jsonify(role)


@ctrl_perm.route("", methods=["POST"])
@ctrl_perm.route("/", methods=["POST"])
@ctrl_perm.route("/<perm_id>", methods=["POST"])
@auth.auth_request
def post_model(perm_id: int = None):
    """POST operation for a Perm model.
    POST /perm
    """
    logging.info("POST RolePerm")
    return ctrl_base.post_model(Perm, perm_id)


@ctrl_perm.route("/<perm_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(perm_id: int = None):
    """DELETE operation for a Image model.
    DELETE /perm
    """
    logging.debug("DELETE Perm")
    return ctrl_base.delete_model(Perm, perm_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_perm.py
