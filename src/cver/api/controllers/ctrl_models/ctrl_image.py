"""
    Cver Api - Controller Model
    Image

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.image import Image
from cver.api.utils import auth

ctrl_image = Blueprint("image", __name__, url_prefix="/image")


@ctrl_image.route("")
@ctrl_image.route("/")
@ctrl_image.route("/<image_id>")
@auth.auth_request
def get_model(image_id: int = None) -> Response:
    """GET operation for a Image.
    GET /image
    """
    image = ctrl_base.get_model(Image, image_id)
    if not isinstance(image, dict):
        return image
    return jsonify(image)


@ctrl_image.route("", methods=["POST"])
@ctrl_image.route("/", methods=["POST"])
@ctrl_image.route("/<image_id>", methods=["POST"])
@auth.auth_request
def post_model(image_id: int = None):
    """POST operation for a Image model.
    POST /image
    """
    logging.info("POST Image")
    return ctrl_base.post_model(Image, image_id)


@ctrl_image.route("/<image_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_id: int = None):
    """DELETE operation for a Image model.
    DELETE /image
    """
    logging.debug("DELETE Image")
    return ctrl_base.delete_model(Image, image_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_image.py
