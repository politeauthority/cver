"""
    Cver Api
    Api Collection - Perms

"""

from flask import Blueprint, jsonify

from cver.api.collects.perms import Perms
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_perms = Blueprint("perms", __name__, url_prefix="/perms")


@ctrl_perms.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Perms)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_perms.py
