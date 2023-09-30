"""
    Cver Api
    Controller Collection
    Clusters

"""

from flask import Blueprint, jsonify

from cver.api.collects.clusters import Clusters
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_clusters = Blueprint("clusters", __name__, url_prefix="/clusters")


@ctrl_clusters.route("")
@ctrl_clusters.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Clusters)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_clusters.py
