"""
    Cver Api
    Controller Collection
    ImageBuildPulls

"""

from flask import Blueprint, jsonify

from cver.api.collects.image_build_pulls import ImageBuildPulls
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_image_build_pulls = Blueprint("image-build-pulls", __name__, url_prefix="/image-build-pulls")


@ctrl_image_build_pulls.route("")
@ctrl_image_build_pulls.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ImageBuildPulls)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_image_build_pulls.py
