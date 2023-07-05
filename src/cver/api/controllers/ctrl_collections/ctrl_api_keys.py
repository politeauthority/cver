"""
    Cver Api - Controller Collection
    Api Keys

"""

from flask import Blueprint, jsonify

from cver.api.collects.api_keys import ApiKeys
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_api_keys = Blueprint("api_keys", __name__, url_prefix="/api-keys")


@ctrl_api_keys.route("")
@auth.auth_request
def index():
    """Get all ApiKeys
    @todo: make the removal of the actual key more generic.
    """
    args = api_util.get_params()
    data = ApiKeys().get_paginated(**args)
    for d in data:
        if "key" in d:
            d.pop("x")
    data["info"]["object_type"] = "api-key"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_api_keys.py
