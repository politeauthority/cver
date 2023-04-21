"""Controller Collection - Cves

"""

from flask import Blueprint, jsonify

from cver.api.collects.cves import Cves

ctrl_cves = Blueprint('cves', __name__, url_prefix='/cves')


@ctrl_cves.route('')
# @auth.auth_request
def index():
    args = {
        "get_json": True
    }
    data = Cves().get_paginated(**args)
    return jsonify(data)

# End File: cver/src/api/controllers/ctrl_collections/ctrl_cves.py
