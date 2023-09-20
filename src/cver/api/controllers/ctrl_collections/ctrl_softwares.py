"""
    Cver Api - Controller Collection
    Softwares

"""

from flask import Blueprint, jsonify

from cver.api.collects.softwares import Softwares
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_softwares = Blueprint('apps', __name__, url_prefix='/apps')


@ctrl_softwares.route('')
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Softwares)
    data["object_type"] = "app"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_softwares.py
