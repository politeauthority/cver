"""
    Cver Api
    Controller Model
    Task

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.task import Task
from cver.api.utils import auth
from cver.api.utils import glow

ctrl_task = Blueprint('task', __name__, url_prefix='/task')


@ctrl_task.route("")
@ctrl_task.route("/")
@ctrl_task.route("/<task_id>")
@auth.auth_request
def get_model(task_id: int = None) -> Response:
    """GET operation for a Task.
    GET /task
    """
    data = ctrl_base.get_model(Task, task_id)
    if not isinstance(data, dict):
        return data
    return jsonify(data)


@ctrl_task.route("", methods=["POST"])
@ctrl_task.route("/", methods=["POST"])
@ctrl_task.route("/<task_id>", methods=["POST"])
@auth.auth_request
def post_model(task_id: int = None):
    """POST operation for a Task model.
    POST /task
    """
    generated_data = {
        "user_id": glow.user["user_id"],
        "org_id": glow.user["user_id"],
    }
    return ctrl_base.post_model(Task, task_id, generated_data=generated_data)


@ctrl_task.route("/<task_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(task_id: int = None):
    """DELETE operation for a Task model.
    DELETE /task
    """
    logging.debug("DELETE task")
    return ctrl_base.delete_model(Task, task_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_task.py
