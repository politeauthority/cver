"""
    Cver Api - Controller Model
    Scan

"""

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.software import Software
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
    data = ctrl_base.get_model(Software, scan_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_scan.py
