"""
    Cver Api - Controller
    Submit-Report

"""
import logging

from flask import Blueprint, jsonify, request

from cver.api.models.image import Image

ctrl_submit_report = Blueprint('submit-report', __name__, url_prefix='/submit-report')


@ctrl_submit_report.route("", methods=["POST"])
# @auth.auth_request
def post_report():
    """POST operation for submit-report."""
    logging.info("Starting submit-report")
    r_args = request.get_json()
    if "image_id" not in r_args:
        logging.warning("No image_id supplied.")
        return error_400()
    image = Image()
    if not image.get_by_id(r_args["image_id"]):
        logging.warning("Image ID %s not found" % r_args["image_id"])
        return error_400()
    logging.info("Working on %s" % image)
    return "hello"


def error_400():
    data = {"status": "error"}
    return jsonify(data), 400

# End File: cve/src/api/controllers/ctrl_submit_report.py
