"""
    Cver Api - Controller Collection
    Softwares

"""

from flask import Blueprint, jsonify, request

from cver.api.collects.softwares import Softwares


ctrl_softwares = Blueprint('apps', __name__, url_prefix='/apps')


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


@ctrl_softwares.route('')
# @auth.auth_request
def index():
    args = get_params()
    data = Softwares().get_paginated(**args)
    data["info"]["object_type"] = "app"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_softwares.py
