"""
    Cver Api - Controller
    Index

"""
from flask import Blueprint, jsonify

from cver.api.utils import glow

ctrl_index = Blueprint("index", __name__, url_prefix="/")


@ctrl_index.route("/")
def index():
    data = {
        "info": "Cver Api",
        "version": glow.general["VERSION"],
        "env": glow.general["CVER_ENV"],
        "build": glow.general["CVER_BUILD"]
    }
    return jsonify(data)

# End File: cve/src/api/controllers/ctrl_index.py
