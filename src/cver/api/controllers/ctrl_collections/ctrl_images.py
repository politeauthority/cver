"""
    Cver Api - Controller Collection
    Images

"""

from flask import Blueprint, jsonify, request

from cver.api.collects.images import Images


ctrl_images = Blueprint("images", __name__, url_prefix="/images")


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


@ctrl_images.route("")
# @auth.auth_request
def index():
    args = get_params()
    data = Images().get_paginated(**args)
    data["info"]["object_type"] = "image"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_images.py
