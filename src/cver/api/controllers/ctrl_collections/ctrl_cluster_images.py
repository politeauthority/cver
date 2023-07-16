"""
    Cver Api - Controller Collection
    ClusterImages

"""

from flask import Blueprint, jsonify

from cver.api.collects.cluster_images import ClusterImages
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_cluster_images = Blueprint("cluster-images", __name__, url_prefix="/cluster-images")


@ctrl_cluster_images.route("")
@ctrl_cluster_images.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(ClusterImages)
    # args = api_util.get_params()
    # data = Images().get_paginated(**args)
    # data["info"]["object_type"] = "image"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_cluster_images.py
