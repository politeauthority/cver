"""
    Cver Api - Controller Model
    Software

"""

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.software import Software
from cver.shared.utils import log
from cver.api.utils import auth

ctrl_software = Blueprint('app', __name__, url_prefix='/app')


@ctrl_software.route("")
@ctrl_software.route("/")
@ctrl_software.route("/<software_id>")
@auth.auth_request
def get_model(software_id: int = None) -> Response:
    """GET operation for a Software.
    GET /app
    """
    data = ctrl_base.get_model(Software, software_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


@ctrl_software.route("", methods=["POST"])
@ctrl_software.route("/", methods=["POST"])
@ctrl_software.route("/<software_id>", methods=["POST"])
@auth.auth_request
def post_model(software_id: int = None):
    """POST operation for a Software model. """
    print("software post")
    return ctrl_base.post_model(Software, software_id)


@ctrl_software.route("<software_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(software_id: int = None):
    """DELETE operation for a Software model. """
    log.debug("software post")
    return ctrl_base.delete_model(Software, software_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_software.py
