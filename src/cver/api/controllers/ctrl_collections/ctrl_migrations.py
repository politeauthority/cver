"""
    Cver Api - Controller Collection
    Images

"""

from flask import Blueprint, jsonify

from cver.api.collects.migrations import Migrations
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_migrations = Blueprint("migrations", __name__, url_prefix="/migrations")


@ctrl_migrations.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Migrations().get_paginated(**args)
    data["info"]["object_type"] = "migration"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_images.py
