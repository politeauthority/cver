"""
    Cver Api - Controller Collection
    ImagesBuilds

"""

from flask import Blueprint, jsonify, request

from cver.api.collects.image_builds import ImageBuilds


ctrl_image_builds = Blueprint("image-builds", __name__, url_prefix="/image-builds")


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


@ctrl_image_builds.route("")
# @auth.auth_request
def index():
    args = get_params()
    data = ImageBuilds().get_paginated(**args)
    data["info"]["object_type"] = "image-build"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_image_builds.py
