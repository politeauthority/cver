#!/usr/bin/env python
"""
    Cver Api
    App

"""
import logging
from logging.config import dictConfig

from flask import Flask, jsonify, request

from cver.api.utils import db
from cver.api.utils import glow

from cver.api.controllers.ctrl_models.ctrl_api_key import ctrl_api_key
from cver.api.controllers.ctrl_collections.ctrl_api_keys import ctrl_api_keys
from cver.api.controllers.ctrl_index import ctrl_index
from cver.api.controllers.ctrl_models.ctrl_image import ctrl_image
from cver.api.controllers.ctrl_collections.ctrl_images import ctrl_images
from cver.api.controllers.ctrl_models.ctrl_image_build import ctrl_image_build
from cver.api.controllers.ctrl_collections.ctrl_image_build_waitings import (
    ctrl_image_build_waitings)
from cver.api.controllers.ctrl_models.ctrl_image_build_waiting import ctrl_image_build_waiting

from cver.api.controllers.ctrl_collections.ctrl_image_builds import ctrl_image_builds
from cver.api.controllers.ctrl_collections.ctrl_migrations import ctrl_migrations
from cver.api.controllers.ctrl_models.ctrl_role import ctrl_role
from cver.api.controllers.ctrl_collections.ctrl_roles import ctrl_roles
from cver.api.controllers.ctrl_models.ctrl_role_perm import ctrl_role_perm
from cver.api.controllers.ctrl_collections.ctrl_role_perms import ctrl_role_perms
from cver.api.controllers.ctrl_models.ctrl_perm import ctrl_perm
from cver.api.controllers.ctrl_collections.ctrl_perms import ctrl_perms
from cver.api.controllers.ctrl_models.ctrl_user import ctrl_user
from cver.api.controllers.ctrl_collections.ctrl_users import ctrl_users
from cver.api.controllers.ctrl_models.ctrl_option import ctrl_option
from cver.api.controllers.ctrl_collections.ctrl_options import ctrl_options
from cver.api.controllers.ctrl_models.ctrl_scan import ctrl_scan
from cver.api.controllers.ctrl_collections.ctrl_scans import ctrl_scans
from cver.api.controllers.ctrl_models.ctrl_software import ctrl_software
from cver.api.controllers.ctrl_collections.ctrl_softwares import ctrl_softwares
from cver.api.controllers.ctrl_submit_scan import ctrl_submit_scan


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

logger = logging.getLogger(__name__)
logger.propagate = True
app = Flask(__name__)
app.config.update(DEBUG=True)
app.debugger = False
glow.db = db.connect()


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    app.register_blueprint(ctrl_api_key)
    app.register_blueprint(ctrl_api_keys)
    app.register_blueprint(ctrl_index)
    app.register_blueprint(ctrl_image)
    app.register_blueprint(ctrl_images)
    app.register_blueprint(ctrl_image_build)
    app.register_blueprint(ctrl_image_builds)
    app.register_blueprint(ctrl_image_build_waiting)
    app.register_blueprint(ctrl_image_build_waitings)
    app.register_blueprint(ctrl_migrations)
    app.register_blueprint(ctrl_roles)
    app.register_blueprint(ctrl_role)
    app.register_blueprint(ctrl_role_perm)
    app.register_blueprint(ctrl_role_perms)
    app.register_blueprint(ctrl_perm)
    app.register_blueprint(ctrl_perms)
    app.register_blueprint(ctrl_user)
    app.register_blueprint(ctrl_users)
    app.register_blueprint(ctrl_option)
    app.register_blueprint(ctrl_options)
    app.register_blueprint(ctrl_scan)
    app.register_blueprint(ctrl_scans)
    app.register_blueprint(ctrl_software)
    app.register_blueprint(ctrl_softwares)
    app.register_blueprint(ctrl_submit_scan)

    return True


@app.errorhandler(Exception)
def handle_exception(e):
    """Catch 500 errors, and pass through the exception
    @todo: Remove the exception for non prod environments.
    """
    data = {
        "message": e,
        "status": "Error: Unhandled Exception"
    }
    return jsonify(data), 500


@app.after_request
def after_request(response):
    logging.info(
        "path: %s | method: %s | status: %s | size: %s",
        request.path,
        request.method,
        response.status,
        response.content_length
    )
    return response


register_blueprints(app)

# Development Runner
if __name__ == "__main__":
    logging.info("Starting develop webserver")
    app.run(host='0.0.0.0', port=80)


# Production Runner
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.debug")
    logging.info("Starting production webserver")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.config['DEBUG'] = True


# End File: cver/src/cver/api/app.py
