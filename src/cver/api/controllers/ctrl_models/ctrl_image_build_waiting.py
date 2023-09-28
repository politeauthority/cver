"""
    Cver Api
    Controller Model
    ImageBuildWaiting

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.image_build_waiting import ImageBuildWaiting
from cver.api.utils import auth

ctrl_image_build_waiting = Blueprint("image-build-waiting", __name__, url_prefix="/image-build-waiting")


@ctrl_image_build_waiting.route("")
@ctrl_image_build_waiting.route("/")
@ctrl_image_build_waiting.route("/<image_build_waiting_id>")
@auth.auth_request
def get_model(image_build_waiting_id: int = None) -> Response:
    """GET operation for a ImageBuildWaiting.
    GET /image-build-waiting
    """
    data = ctrl_base.get_model(ImageBuildWaiting, image_build_waiting_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_image_build_waiting.route("", methods=["POST"])
@ctrl_image_build_waiting.route("/", methods=["POST"])
@ctrl_image_build_waiting.route("/<image_build_waiting_id>", methods=["POST"])
@auth.auth_request
def post_model(image_build_waiting_id: int = None):
    """POST operation for a ImageBuildWaiting model.
    POST /image-build-waiting
    """
    logging.info("POST ImageBuild")
    return ctrl_base.post_model(ImageBuildWaiting, image_build_waiting_id)


@ctrl_image_build_waiting.route("/<image_build_waiting_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(image_build_waiting_id: int = None):
    """DELETE operation for a ImageBuildWaiting model.
    DELETE /image-build-waiting
    """
    logging.debug("DELETE ImageBuild")
    return ctrl_base.delete_model(ImageBuildWaiting, image_build_waiting_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_image_build_waiting.py
