"""
    Cver Api
    Controller Model
    Scan Raw

"""

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.scan_raw import ScanRaw
from cver.api.utils import auth

ctrl_scan_raw = Blueprint('scan-raw', __name__, url_prefix='/scan-raw')


@ctrl_scan_raw.route("")
@ctrl_scan_raw.route("/")
@ctrl_scan_raw.route("/<scan_raw_id>")
@auth.auth_request
def get_model(scan_raw_id: int = None) -> Response:
    """GET operation for a ScanRaw.
    GET /scan-raw
    """
    data = ctrl_base.get_model(ScanRaw, scan_raw_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_scan_raw.route("", methods=["POST"])
@ctrl_scan_raw.route("/", methods=["POST"])
@ctrl_scan_raw.route("/<scan_raw_id>", methods=["POST"])
@auth.auth_request
def post_model(scan_raw_id: int = None):
    """POST operation for a Scan model.
    POST /scan-raw
    """
    return ctrl_base.post_model(ScanRaw, scan_raw_id)


@ctrl_scan_raw.route("/<scan_raw_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(scan_raw_id: int = None):
    """DELETE operation for a Scan model.
    DELETE /scan-raw
    """
    return ctrl_base.delete_model(ScanRaw, scan_raw_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_scan_raw.py
