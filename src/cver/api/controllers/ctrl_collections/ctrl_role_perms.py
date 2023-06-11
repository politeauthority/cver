"""
    Cver Api
    Api Collection - RolePerms

"""

from flask import Blueprint, jsonify

from cver.api.collects.roles import Roles
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_role_perms = Blueprint("role_perms", __name__, url_prefix="/role-perms")


@ctrl_role_perms.route("")
@auth.auth_request
def index():
    args = api_util.get_params()
    data = Roles().get_paginated(**args)
    data["info"]["object_type"] = "role-perm"
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_role_perms.py
