"""
    Cver Api - Controller Collection
    ImagesBuilds

"""

from flask import Blueprint, jsonify

from cver.api.collects.image_builds import ImageBuilds
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_image_builds = Blueprint("image-builds", __name__, url_prefix="/image-builds")


@ctrl_image_builds.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ImageBuilds)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_image_builds.py
