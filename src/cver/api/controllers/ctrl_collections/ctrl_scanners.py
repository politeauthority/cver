"""
    Cver Api - Controller Collection
    Scanners

"""

from flask import Blueprint, jsonify

from cver.api.collects.scanners import Scanners
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_scanners = Blueprint("scanners", __name__, url_prefix="/scanners")


@ctrl_scanners.route("")
@ctrl_scanners.route("/")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Scanners().get_paginated(**args)
    data["info"]["object_type"] = "scanner"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_scanners.py
