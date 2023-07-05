"""
    Cver Api - Controller Collection
    Scans

"""

from flask import Blueprint, jsonify

from cver.api.collects.scans import Scans
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_scans = Blueprint("scans", __name__, url_prefix="/scans")


@ctrl_scans.route("")
@ctrl_scans.route("/")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Scans().get_paginated(**args)
    data["info"]["object_type"] = "scans"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_scans.py
