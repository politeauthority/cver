"""
    Cver Api
    Controller Collection
    Registries

"""

from flask import Blueprint, jsonify

from cver.api.collects.registries import Registries
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_registries = Blueprint("registries", __name__, url_prefix="/registries")


@ctrl_registries.route("")
@ctrl_registries.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Registries)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_registries.py
