"""Controller Model - Vendor

"""

from flask import Blueprint, request, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.vendor import Vendor
# from pignus_api.utils import auth
from cver.api.utils import misc
from cver.shared.utils import log

ctrl_vendor = Blueprint('vendor', __name__, url_prefix='/vendor')


@ctrl_vendor.route("")
@ctrl_vendor.route("/<vendor_id>")
# @auth.auth_request
def get_model(vendor_id: int = None) -> Response:
    """GET operation for a Vendor.
    GET /image
    """
    data = ctrl_base.get_model(Vendor, vendor_id)
    if not isinstance(data, dict):
        return data

    return jsonify(data)


# End File: cve/src/api/controllers/ctrl_modles/ctrl_vendor.py
