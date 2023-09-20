"""
    Cver Api - Controller Collection
    Options

"""

from flask import Blueprint, jsonify

from cver.api.collects.options import Options
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Options)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_options.py
