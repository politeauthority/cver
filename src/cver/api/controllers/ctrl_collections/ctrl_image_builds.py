"""
    Cver Api - Controller Collection
    ImagesBuilds

"""

from flask import Blueprint, jsonify, request

from cver.api.utils import api_util
from cver.api.collects.image_builds import ImageBuilds


ctrl_image_builds = Blueprint("image-builds", __name__, url_prefix="/image-builds")


@ctrl_image_builds.route("")
# @auth.auth_request
def index():
    args = api_util.get_params()
    data = ImageBuilds().get_paginated(**args)
    data["info"]["object_type"] = "image-build"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_image_builds.py
