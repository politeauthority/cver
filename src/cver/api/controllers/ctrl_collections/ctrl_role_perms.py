"""
    Cver Api
    Api Collection - RolePerms

"""

from flask import Blueprint, jsonify

from cver.api.collects.role_perms import RolePerms
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_role_perms = Blueprint("role_perms", __name__, url_prefix="/role-perms")


@ctrl_role_perms.route("")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(RolePerms)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_role_perms.py
