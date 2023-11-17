"""
    Cver Api
    Controller Model
    Registry

"""
import logging

from flask import Blueprint, jsonify, Response

from cver.api.controllers.ctrl_models import ctrl_base
from cver.api.models.registry import Registry
from cver.api.utils import auth

ctrl_registry = Blueprint("registry", __name__, url_prefix="/registry")


@ctrl_registry.route("")
@ctrl_registry.route("/")
@ctrl_registry.route("/<registry_id>")
@auth.auth_request
def get_model(registry_id: int = None) -> Response:
    """GET operation for a Registry.
    GET /registry
    """
    image = ctrl_base.get_model(Registry, registry_id)
    if not isinstance(image, dict):
        return image
    return jsonify(image)


@ctrl_registry.route("", methods=["POST"])
@ctrl_registry.route("/", methods=["POST"])
@ctrl_registry.route("/<registry_id>", methods=["POST"])
@auth.auth_request
def post_model(registry_id: int = None):
    """POST operation for a Registry model.
    POST /registry
    """
    logging.info("POST Image")
    return ctrl_base.post_model(Registry, registry_id)


@ctrl_registry.route("/<registry_id>", methods=["DELETE"])
@auth.auth_request
def delete_model(registry_id: int = None):
    """DELETE operation for a Registry model.
    DELETE /registry
    """
    logging.debug("DELETE Registry")
    return ctrl_base.delete_model(Registry, registry_id)


# End File: cve/src/api/controllers/ctrl_models/ctrl_image.py
