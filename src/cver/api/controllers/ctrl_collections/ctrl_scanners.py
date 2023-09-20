"""
    Cver Api - Controller Collection
    Scanners

"""

from flask import Blueprint, jsonify

from cver.api.collects.scanners import Scanners
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_scanners = Blueprint("scanners", __name__, url_prefix="/scanners")


@ctrl_scanners.route("")
@ctrl_scanners.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Scanners)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_scanners.py
