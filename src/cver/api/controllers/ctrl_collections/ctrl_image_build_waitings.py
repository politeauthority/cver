"""
    Cver Api - Controller Collection
    ImagesBuildWaitings

"""

from flask import Blueprint, jsonify

from cver.api.collects.image_build_waitings import ImageBuildWaitings
from cver.api.controllers.ctrl_collections import ctrl_collection_base
# from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_image_build_waitings = Blueprint(
    "image-build-waitings",
    __name__,
    url_prefix="/image-build-waitings")


@ctrl_image_build_waitings.route("")
@ctrl_image_build_waitings.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ImageBuildWaitings)
    # args = api_util.get_params()
    # data = ImageBuildWaitings().get_paginated(**args)
    # data["info"]["object_type"] = "image-build-waiting"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_image_build_waitings.py
