"""
    Cver Api
    Controller Collection
    Scan Raws

"""

from flask import Blueprint, jsonify

from cver.api.collects.scan_raws import ScanRaws
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_scan_raws = Blueprint("scan-raws", __name__, url_prefix="/scan-raws")


@ctrl_scan_raws.route("")
@ctrl_scan_raws.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ScanRaws)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_scan_raws.py
