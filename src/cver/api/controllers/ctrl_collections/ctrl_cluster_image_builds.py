"""
    Cver Api -
    Controller Collection
    Cluster Images Builds

"""

from flask import Blueprint, jsonify

from cver.api.collects.cluster_image_builds import ClusterImageBuilds
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_cluster_image_builds = Blueprint(
    "cluster-image-builds", __name__, url_prefix="/cluster-image-builds")


@ctrl_cluster_image_builds.route("")
@ctrl_cluster_image_builds.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ClusterImageBuilds)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_cluster_image_builds.py
