"""
    Cver Api - Controller Collection
    Users

"""

from flask import Blueprint, jsonify

from cver.api.collects.users import Users
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_users = Blueprint("users", __name__, url_prefix="/users")


@ctrl_users.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Users)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_users.py
