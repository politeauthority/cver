"""
    Cver Api - Controller Collection
    Softwares

"""

from flask import Blueprint, jsonify

from cver.api.collects.softwares import Softwares
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_softwares = Blueprint('apps', __name__, url_prefix='/apps')


@ctrl_softwares.route('')
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Softwares().get_paginated(**args)
    data["info"]["object_type"] = "app"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_softwares.py
