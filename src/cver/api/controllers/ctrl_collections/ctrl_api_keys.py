"""
    Cver Api - Controller Collection
    Api Keys

"""

from flask import Blueprint, jsonify

from cver.api.utils import api_util
from cver.api.collects.api_keys import ApiKeys
from cver.api.utils import auth

ctrl_api_keys = Blueprint("api_keys", __name__, url_prefix="/api-keys")


@ctrl_api_keys.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    print(args)
    data = ApiKeys().get_paginated(**args)
    data["info"]["object_type"] = "api-key"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_api_keys.py
