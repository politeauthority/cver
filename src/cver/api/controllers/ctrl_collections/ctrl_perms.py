"""
    Cver Api
    Api Collection - Perms

"""

from flask import Blueprint, jsonify

from cver.api.collects.perms import Perms
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_perms = Blueprint("perms", __name__, url_prefix="/perms")


@ctrl_perms.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Perms().get_paginated(**args)
    data["info"]["object_type"] = "perm"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_perms.py
