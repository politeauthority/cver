"""
    Cver Api - Controller Collection
    Options

"""

from flask import Blueprint, jsonify

from cver.api.collects.options import Options
from cver.api.utils import api_util
from cver.api.utils import auth

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
@auth.auth_request
def index():
    args = api_util.get_params()
    options_data = Options().get_paginated(**args)
    return jsonify(options_data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_options.py
