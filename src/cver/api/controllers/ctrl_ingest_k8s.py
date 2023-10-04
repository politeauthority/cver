"""
    Cver Api - Controller
    Ingest Kubernetes
    These routes serve to take input from the Kubernetes ingestion scripts.

"""
import json
import logging

from flask import Blueprint, request, make_response, jsonify

from cver.api.utils import auth
from cver.api.models.cluster import Cluster
from cver.api.models.cluster_image import ClusterImage
from cver.api.models.image_build import ImageBuild
from cver.api.models.image_build_waiting import ImageBuildWaiting
from cver.api.models.image import Image
from cver.shared.utils import misc
from cver.shared.utils import date_utils


ctrl_ingest_k8s = Blueprint("ingest-k8s", __name__, url_prefix="/ingest-k8s")


@ctrl_ingest_k8s.route("image", methods=["POST"])
@ctrl_ingest_k8s.route("/image", methods=["POST"])
@auth.auth_request
def post_submit_image():
    """POST operation for submit-scan."""
    logging.info("Starting - Ingest K8s Image")

    data = {
        "message": "",
        "wrote": {},
        "status": "success"
    }
    required_keys = ["cluster_id", "image"]
    request_json = request.get_json()
    for required_key in required_keys:
        if required_key not in request_json:
            data["message"] = f'Missing required data key, "{required_key}" to submit a scan'
            data["status"] = "error"
            return make_response(json.dumps(data), 401)

    # Make sure we have our Cluster
    cluster_id = request_json["cluster_id"]
    cluster = Cluster()
    if not cluster.get_by_id(cluster_id):
        data["message"] = f"Invalid Cluster ID: {cluster_id}"
        data["status"] = "error"
        return make_response(json.dumps(data), 400)

    # Handle Image
    image_map = misc.container_url(request_json["image"])
    image = Image()
    if not image.get_by_repo_and_name(image_map["repository"], image_map["image"]):
        image.repository = image_map["repository"]
        image.name = image_map["image"]
        image.save()
        data["wrote"]["image"] = image.json()

    ibx = _handle_image_build(image, image_map)
    if ibx:
        if isinstance(ibx, ImageBuild):
            data["wrote"]["image-build"] = ibx.json()
        elif isinstance(ibx, ImageBuildWaiting):
            data["wrote"]["image-build-waiting"] = ibx.json()

    # Handle Cluster Image
    ic = _handle_cluster_image(cluster_id, image.id)
    if ic:
        data["wrote"]["image-cluster"] = ic.json()

    return jsonify(data), 201


def _handle_image_build(image: Image, image_map: dict) -> ImageBuildWaiting:
    if "sha" in image_map and image_map["sha"]:
        ib = ImageBuild()
        ib.sha = image_map["sha"]
        ib.image_id = image.id
        ib.repository = image_map["repository"]
        if "tag" in image_map and image_map["tag"]:
            ib.tags = [image_map["tag"]]
        ib.save()
        return ib
    else:
        ibw = ImageBuildWaiting()
        fields = {
            "image_id": image.id,
            "image_build_id": None,
            "tag": image_map["tag"]
        }
        if ibw.get_by_unique_key(fields):
            return ibw
        ibw.image_id = image.id
        ibw.waiting_for = "download"
        if "tag" in image_map and image_map["tag"]:
            ibw.tag = image_map["tag"]
        ibw.save()
        return ibw


def _handle_cluster_image(cluster_id: int, image_id: int) -> bool:
    """Check if the Cluster Image relationship already exists, if not create it, then update the
    last seen date.
    """
    cluster_image = ClusterImage()
    if not cluster_image.get_by_cluster_and_image_id(cluster_id, image_id):
        cluster_image.cluster_id = cluster_id
        cluster_image.image_id = image_id
        cluster_image.first_seen = date_utils.now()
    cluster_image.last_seen = date_utils.now()
    cluster_image.save()
    return cluster_image

# End File: cve/src/api/controllers/ctrl_ingest_k8s.py
