"""
    Cver Api - Controller Collection
    Users

"""

from flask import Blueprint, jsonify, request

from cver.api.collects.users import Users
from cver.api.utils import auth

ctrl_users = Blueprint("users", __name__, url_prefix="/users")


def get_params() -> dict:
    args = {
        "page": 1,
        "per_page": 20,
        "get_json": True,
    }
    raw_args = request.args
    if "p" in raw_args and raw_args["p"].isdigit():
        args["page"] = int(raw_args["p"])
    return args


@ctrl_users.route("")
@auth.auth_request
def index():
    args = get_params()
    data = Users().get_paginated(**args)
    data["info"]["object_type"] = "user"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_users.py
