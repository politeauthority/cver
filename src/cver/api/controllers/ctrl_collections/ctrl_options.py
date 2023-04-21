"""Controller Collection - Options

"""

from flask import Blueprint, jsonify

from cver.api.collects.options import Options

ctrl_options = Blueprint('options', __name__, url_prefix='/options')


@ctrl_options.route('')
# @auth.auth_request
def index():
    options_data = Options().get_paginated(get_json=True)
    return jsonify(options_data)

# End File: cver/src/api/controllers/ctrl_collections/ctrl_options.py
