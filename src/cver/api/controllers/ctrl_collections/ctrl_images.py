"""
    Cver Api - Controller Collection
    Images

"""

from flask import Blueprint, jsonify

from cver.api.collects.images import Images
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_images = Blueprint("images", __name__, url_prefix="/images")


@ctrl_images.route("")
@ctrl_images.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Images)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_images.py
