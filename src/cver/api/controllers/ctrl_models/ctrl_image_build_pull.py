"""
    Cver Api
    Controller Model
    ImageBuildPull

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.image_build_pull import ImageBuildPull
from cver.api.utils import auth

ctrl_image_build_pull = Blueprint("image-build-pull", __name__, url_prefix="/image-build-pull")


@ctrl_image_build_pull.route("")
@ctrl_image_build_pull.route("/")
@ctrl_image_build_pull.route("/<image_build_pull_id>")
@auth.auth_request
def get_model(image_build_pull_id: int = None) -> Response:
    """GET operation for a ImageBuildPull.
    GET /image-build-pull
    """
    image = ctrl_base.get_model(ImageBuildPull, image_build_pull_id)
    if not isinstance(image, dict):
        return image
    return jsonify(image)


@ctrl_image_build_pull.route("", methods=["POST"])
@ctrl_image_build_pull.route("/", methods=["POST"])
@ctrl_image_build_pull.route("/<image_build_pull_id>", methods=["POST"])
@auth.auth_request
def post_model(image_build_pull_id: int = None):
    """POST operation for a ImageBuildPull model.
    POST /image-build-pull
    """
    logging.info("POST Image")
    return ctrl_base.post_model(ImageBuildPull, image_build_pull_id)


@ctrl_image_build_pull.route("/<image_build_pull_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_build_pull_id: int = None):
    """DELETE operation for a ImageBuildPull model.
    DELETE /image-build-pull
    """
    logging.debug("DELETE Image")
    return ctrl_base.delete_model(ImageBuildPull, image_build_pull_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_image_build_pull.py
