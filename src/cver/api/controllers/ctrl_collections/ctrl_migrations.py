"""
    Cver Api - Controller Collection
    Images

"""

from flask import Blueprint, jsonify

from cver.api.collects.migrations import Migrations
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_migrations = Blueprint("migrations", __name__, url_prefix="/migrations")


@ctrl_migrations.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Migrations)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_images.py
