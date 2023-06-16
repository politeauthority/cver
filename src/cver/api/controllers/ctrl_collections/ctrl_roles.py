"""
    Cver Api
    Api Collection - Roles

"""

from flask import Blueprint, jsonify

from cver.api.collects.roles import Roles
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_roles = Blueprint("roles", __name__, url_prefix="/roles")


@ctrl_roles.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Roles().get_paginated(**args)
    data["info"]["object_type"] = "role"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_roles.py
