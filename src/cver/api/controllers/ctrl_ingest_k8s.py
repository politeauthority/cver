"""
    Cver Api - Controller
    Ingest Kubernetes

"""
import json
import logging

from flask import Blueprint, request, make_response

from cver.api.utils import auth
from cver.api.models.cluster import Cluster
from cver.api.models.image import Image
# from cver.api.models.image_build import ImageBuild
# from cver.api.models.scan import Scan
# # from cver.api.models.scan_raw import ScanRaw
# from cver.api.utils import date_utils
# from cver.api.utils import parse_trivy


ctrl_ingest_k8s = Blueprint("ingest-k8s", __name__, url_prefix="/ingest-k8s")


@ctrl_ingest_k8s.route("image", methods=["POST"])
@ctrl_ingest_k8s.route("/image", methods=["POST"])
@auth.auth_request
def post_submit_image():
    """POST operation for submit-scan."""
    logging.info("Starting - Ingest K8s Image")

    data = {
        "message": "",
        "status": "Success"
    }
    required_keys = ["cluster_id", "image"]
    request_json = request.get_json()
    for required_key in required_keys:
        if required_key not in request_json:
            data["message"] = f'Missing required data key, "{required_key}" to submit a scan'
            data["status"] = "error"
            return make_response(json.dumps(data), 401)

    cluster_id = request_json["cluster_id"]
    cluster = Cluster()
    if not cluster.get_by_id(cluster_id):
        data["message"] = f'Invalid Cluster ID: {cluster_id}'
        data["status"] = "error"
        return make_response(json.dumps(data), 401)

    image_name = request_json["image"]
    image = Image()
    if not image.get_by_name(image_name):
        image.name = image_name
    # print(image_data)


# End File: cve/src/api/controllers/ctrl_ingest_k8s.py
