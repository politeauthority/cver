"""
    Cver Api - Controller Model
    Cluster

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.cluster import Cluster
from cver.api.utils import auth

ctrl_cluster = Blueprint("cluster", __name__, url_prefix="/cluster")


@ctrl_cluster.route("")
@ctrl_cluster.route("/")
@ctrl_cluster.route("/<image_id>")
@auth.auth_request
def get_model(image_id: int = None) -> Response:
    """GET operation for a Cluster.
    GET /cluster
    """
    cluster = ctrl_base.get_model(Cluster, image_id)
    if not isinstance(cluster, dict):
        return cluster
    return jsonify(cluster)


@ctrl_cluster.route("", methods=["POST"])
@ctrl_cluster.route("/", methods=["POST"])
@ctrl_cluster.route("/<cluster_id>", methods=["POST"])
@auth.auth_request
def post_model(cluster_id: int = None):
    """POST operation for a Cluster model.
    POST /cluster
    """
    logging.info("POST Cluster")
    return ctrl_base.post_model(Cluster, cluster_id)


@ctrl_cluster.route("/<cluster_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(cluster_id: int = None):
    """DELETE operation for a Image model.
    DELETE /cluster
    """
    logging.debug("DELETE Cluster")
    return ctrl_base.delete_model(Cluster, cluster_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_cluster.py
