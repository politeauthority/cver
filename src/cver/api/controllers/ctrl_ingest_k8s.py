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
    required_keys = ["cluster_id", "image", "sha"]
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
    if image_map["sha"]:
        return jsonify(data), 200
    if not image_map["sha"] and request_json["sha"]:
        image_map["sha"] = request_json["sha"]
    image = Image()
    if not image.get_by_registry_and_name(image_map["registry"], image_map["image"]):
        image.registry = image_map["registry"]
        image.name = image_map["image"]
        image.save()
        data["wrote"]["image"] = image.json()

    ibx = _handle_image_build(image, image_map)
    if ibx["image-build"]:
        data["wrote"]["image-build"] = ibx["image-build"].json()

    # Handle Cluster Image
    ic = _handle_cluster_image(cluster_id, image.id)
    if ic:
        data["wrote"]["image-cluster"] = ic.json()

    return jsonify(data), 201


def _handle_image_build(image: Image, image_map: dict) -> ImageBuildWaiting:
    """Handles building an ImageBuildWaiting and ImageBuild if possible.
    :@todo: This is a mess, clean this up.
    """
    ret = {
        "image-build": None,
        # "image-build-waiting": None
    }
    if "sha" in image_map and image_map["sha"]:
        ib = ImageBuild()
        ib.sha = image_map["sha"]
        found = ib.get_by_sha()
        if not found:
            ib.image_id = image.id
            ib.registry = image_map["registry"]
            ib.sync_flag = True
            ib.scan_flag = True
            if "tag" in image_map and image_map["tag"]:
                ib.tags = [image_map["tag"]]
            ib.save()
        found = False
        ret["image-build"] = ib

    # ibw = ImageBuildWaiting()
    # fields = [
    #     {
    #         "field": "image_id",
    #         "value": image.id,
    #         "op": "eq"
    #     },
    #     {
    #         "field": "tag",
    #         "value": image_map["tag"],
    #         "op": "eq"
    #     },
    # ]

    # if image_map["sha"]:
    #     ibw.sha = image_map["sha"]
    #     found = ibw.get_by_sha()
    # else:
    #     found = ibw.get_by_fields(fields)

    # if found:
    #     logging.info("Found IBW: %s" % ibw)
    #     ret["image-build-waiting"] = ibw
    #     return ret

    # if ret["image-build"]:
    #     ibw.image_build_id = ret["image-build"].id

    # ibw.image_id = image.id
    # ibw.waiting_for = "download"
    # if "tag" in image_map and image_map["tag"]:
    #     ibw.tag = image_map["tag"]
    # ibw.save()
    # ret["image-build-waiting"] = ibw
    return ret


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
