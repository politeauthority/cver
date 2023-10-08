"""
    Cver Api
    Controller Collection
    Tasks

"""

from flask import Blueprint, jsonify

from cver.api.collects.tasks import Tasks
from cver.api.controllers.ctrl_collections import ctrl_collection_base
from cver.api.utils import auth

ctrl_tasks = Blueprint("tasks", __name__, url_prefix="/tasks")


@ctrl_tasks.route("")
@ctrl_tasks.route("/")
@auth.auth_request
def index():
    data = ctrl_collection_base.get(Tasks)
    return jsonify(data)


# End File: cver/src/api/controllers/ctrl_collections/ctrl_tasks.py
