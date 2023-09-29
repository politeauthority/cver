"""
    Cver Api - Controller Collection
    Scans

"""

from flask import Blueprint, jsonify

from cver.api.collects.scans import Scans
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_scans = Blueprint("scans", __name__, url_prefix="/scans")


@ctrl_scans.route("")
@ctrl_scans.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Scans)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_scans.py
