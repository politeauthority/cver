"""
    Cver Api - Controller
    Submit-Scan
    Ingestion point for ImageBuild scans to be recored with.

"""
import json
import logging

from flask import Blueprint, jsonify, request, make_response

from cver.api.models.image import Image
from cver.api.models.image_build import ImageBuild
from cver.api.models.scan import Scan
# from cver.api.models.scan_raw import ScanRaw
from cver.api.utils import auth
from cver.api.utils import date_utils
from cver.api.utils import parse_trivy


ctrl_submit_scan = Blueprint('submit-scan', __name__, url_prefix='/submit-scan')


@ctrl_submit_scan.route("", methods=["POST"])
@ctrl_submit_scan.route("/", methods=["POST"])
@auth.auth_request
def post_sumit_scan():
    """POST operation for submit-scan."""
    data = {
        "message": "",
        "status": "Success"
    }
    logging.info("Starting submit-report")

    # Check that we have the needed data
    required_keys = ["image_id", "image_build_id", "scanner_id", "raw"]
    request_json = request.get_json()
    for required_key in required_keys:
        if required_key not in request_json:
            data["message"] = f'Missing required data key, "{required_key}" to submit a scan'
            data["status"] = "Error"
            return make_response(json.dumps(data), 401)

    # Get the Image
    image = Image()
    if not image.get_by_id(request_json["image_id"]):
        data["message"] = "Unknown Image ID"
        data["status"] = "Error"
        return make_response(json.dumps(data), 404)

    # Get the ImageBuild
    image_build = ImageBuild()
    if not image_build.get_by_id(request_json["image_build_id"]):
        data["message"] = "Unknown ImageBuild ID"
        data["status"] = "Error"
        return make_response(json.dumps(data), 404)

    # Parse the scan
    parsed_scan = parse_trivy.parse(request_json["raw"])

    print("\n\nPARSED")
    print(parsed_scan)
    print("\n\n")
    # Create the Scan
    scan = Scan()
    scan.image_id = image.id
    scan.image_build_id = image_build.id
    scan.cve_critical_int = parsed_scan["cve_critical_int"]
    scan.cve_critical_nums = parsed_scan["cve_critical_nums"]

    scan.cve_high_int = parsed_scan["cve_high_int"]
    scan.cve_high_nums = parsed_scan["cve_high_nums"]

    scan.cve_medium_int = parsed_scan["cve_medium_int"]
    scan.cve_medium_nums = parsed_scan["cve_medium_nums"]

    scan.cve_low_int = parsed_scan["cve_low_int"]
    scan.cve_low_nums = parsed_scan["cve_low_nums"]
    scan.save()

    # # Create the ScanRaw
    # scan_raw = ScanRaw()
    # scan_raw.image_id = image.id
    # scan_raw.image_build_id = image_build.id
    # scan_raw.scanner_id = request_json["scanner_id"]
    # scan_raw.scan_id = scan.id
    # scan_raw.raw = request_json["raw"]
    # scan_raw.insert()

    image_build.scan_lat_ts = date_utils.now()
    image_build.save()

    logging.info(f"Saved scan for {image} {image_build} {scan}")

    return jsonify(data), 201


def error_400():
    data = {"status": "error"}
    return jsonify(data), 400

# End File: cve/src/api/controllers/ctrl_submit_scan.py
