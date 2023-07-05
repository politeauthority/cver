"""
    Cver Api - Controller Collection
    Users

"""

from flask import Blueprint, jsonify

from cver.api.collects.users import Users
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_users = Blueprint("users", __name__, url_prefix="/users")


@ctrl_users.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Users().get_paginated(**args)
    data["info"]["object_type"] = "user"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_users.py
