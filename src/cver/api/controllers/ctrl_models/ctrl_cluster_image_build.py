"""
    Cver Api - Controller Model
    ClusterImage

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.cluster_image_build import ClusterImageBuild
from cver.api.utils import auth

ctrl_cluster_image_build = Blueprint(
    "cluster-image-build", __name__, url_prefix="/cluster-image-build")


@ctrl_cluster_image_build.route("/")
@ctrl_cluster_image_build.route("/")
@ctrl_cluster_image_build.route("/<cluster_image_build_id>")
@auth.auth_request
def get_model(cluster_image_build_id: int = None) -> Response:
    """GET operation for an entity.
    GET /cluster-image-build
    """
    image = ctrl_base.get_model(ClusterImageBuild, cluster_image_build_id)
    if not isinstance(image, dict):
        return image
    return jsonify(image)


@ctrl_cluster_image_build.route("", methods=["POST"])
@ctrl_cluster_image_build.route("/", methods=["POST"])
@ctrl_cluster_image_build.route("/<cluster_image_build_id>", methods=["POST"])
@auth.auth_request
def post_model(cluster_image_build_id: int = None):
    """POST operation for an entity.
    POST /cluster-image-build
    """
    logging.info("POST ClusterImage")
    return ctrl_base.post_model(ClusterImageBuild, cluster_image_build_id)


@ctrl_cluster_image_build.route("", methods=["DELETE"])
@ctrl_cluster_image_build.route("/", methods=["DELETE"])
@ctrl_cluster_image_build.route("/<cluster_image_build_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(cluster_image_build_id: int = None):
    """DELETE operation for a Image model.
    DELETE /cluster-image-build
    """
    logging.debug("DELETE ClusterImage")
    return ctrl_base.delete_model(ClusterImageBuild, cluster_image_build_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_cluster_image_build.py
