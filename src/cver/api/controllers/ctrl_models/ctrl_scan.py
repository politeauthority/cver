"""
    Cver Api - Controller Model
    Scan

"""

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.scan import Scan
from cver.api.utils import auth

ctrl_scan = Blueprint('scan', __name__, url_prefix='/scan')


@ctrl_scan.route("")
@ctrl_scan.route("/")
@ctrl_scan.route("/<scan_id>")
@auth.auth_request
def get_model(scan_id: int = None) -> Response:
    """GET operation for a Scan.
    GET /scan
    """
    data = ctrl_base.get_model(Scan, scan_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_scan.route("", methods=["POST"])
@ctrl_scan.route("/", methods=["POST"])
@ctrl_scan.route("/<scan_id>", methods=["POST"])
@auth.auth_request
def post_model(scan_id: int = None):
    """POST operation for a Scan model.
    POST /scan
    """
    return ctrl_base.post_model(Scan, scan_id)


@ctrl_scan.route("/<scan_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(scan_id: int = None):
    """DELETE operation for a Scan model.
    DELETE /scan
    """
    return ctrl_base.delete_model(Scan, scan_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_scan.py
