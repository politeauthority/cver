"""
    Cver Api - Controller Model
    Image-Build

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.image_build import ImageBuild
from cver.api.utils import auth

ctrl_image_build = Blueprint("image-build", __name__, url_prefix="/image-build")


@ctrl_image_build.route("")
@ctrl_image_build.route("/")
@ctrl_image_build.route("/<image_build_id>")
@auth.auth_request
def get_model(image_build_id: int = None) -> Response:
    """GET operation for a Image.
    GET /image-build
    """
    data = ctrl_base.get_model(ImageBuild, image_build_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_image_build.route("", methods=["POST"])
@ctrl_image_build.route("/", methods=["POST"])
@ctrl_image_build.route("/<image_build_id>", methods=["POST"])
@auth.auth_request
def post_model(image_build_id: int = None):
    """POST operation for a ImageBuild model.
    POST /image-build
    """
    logging.info("POST ImageBuild")
    return ctrl_base.post_model(ImageBuild, image_build_id)


@ctrl_image_build.route("/<image_build_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_build_id: int = None):
    """DELETE operation for a ImageBuild model.
    DELETE /image-build
    """
    logging.debug("DELETE ImageBuild")
    return ctrl_base.delete_model(ImageBuild, image_build_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_image_build.py
