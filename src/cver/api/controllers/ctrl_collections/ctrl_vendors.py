"""Controller Collection - Vendors

"""

from flask import Blueprint, jsonify, request

from cver.api.collects.vendors import Vendors


ctrl_vendors = Blueprint('vendors', __name__, url_prefix='/vendors')


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


@ctrl_vendors.route('')
# @auth.auth_request
def index():
    args = get_params()
    vendor_data = Vendors().get_paginated(**args)
    return jsonify(vendor_data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_vendors.py
