"""
    Cver Api - Controller Model
    ClusterImage

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.cluster_image import ClusterImage
from cver.api.utils import auth

ctrl_cluster_image = Blueprint("cluster-image", __name__, url_prefix="/cluster-image")


@ctrl_cluster_image.route("")
@ctrl_cluster_image.route("/")
@ctrl_cluster_image.route("/<cluster_image_id>")
@auth.auth_request
def get_model(cluster_image_id: int = None) -> Response:
    """GET operation for an entity.
    GET /cluster-image
    """
    image = ctrl_base.get_model(ClusterImage, cluster_image_id)
    if not isinstance(image, dict):
        return image
    return jsonify(image)


@ctrl_cluster_image.route("", methods=["POST"])
@ctrl_cluster_image.route("/", methods=["POST"])
@ctrl_cluster_image.route("/<cluster_image_id>", methods=["POST"])
@auth.auth_request
def post_model(cluster_image_id: int = None):
    """POST operation for an entity.
    POST /cluster-image
    """
    logging.info("POST ClusterImage")
    return ctrl_base.post_model(ClusterImage, cluster_image_id)


@ctrl_cluster_image.route("", methods=["DELETE"])
@ctrl_cluster_image.route("/", methods=["DELETE"])
@ctrl_cluster_image.route("/<cluster_image_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(cluster_image_id: int = None):
    """DELETE operation for a Image model.
    DELETE /cluster-image
    """
    logging.debug("DELETE ClusterImage")
    return ctrl_base.delete_model(ClusterImage, cluster_image_id)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_cluster_image.py
