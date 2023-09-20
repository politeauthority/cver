"""
    Cver Api
    Api Collection - Roles

"""

from flask import Blueprint, jsonify

from cver.api.collects.roles import Roles
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_roles = Blueprint("roles", __name__, url_prefix="/roles")


@ctrl_roles.route("")
@auth.auth_request
def index():
    """Get Roles."""
    data = ctrl_collection_base.get(Roles)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_roles.py
