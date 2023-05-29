#!/usr/bin/env python
"""
    Cver Api
    App

"""
import json
import logging
from logging.config import dictConfig


from flask import Flask
from werkzeug.exceptions import HTTPException

from cver.api.utils import db
from cver.api.utils import glow

from cver.api.controllers.ctrl_index import ctrl_index
from cver.api.controllers.ctrl_models.ctrl_image import ctrl_image
from cver.api.controllers.ctrl_collections.ctrl_images import ctrl_images
from cver.api.controllers.ctrl_models.ctrl_image_build import ctrl_image_build
from cver.api.controllers.ctrl_collections.ctrl_image_builds import ctrl_image_builds
from cver.api.controllers.ctrl_collections.ctrl_options import ctrl_options
from cver.api.controllers.ctrl_collections.ctrl_softwares import ctrl_softwares
from cver.api.controllers.ctrl_models.ctrl_software import ctrl_software
from cver.api.controllers.ctrl_submit_report import ctrl_submit_report


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

app = Flask(__name__)


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    # app.register_blueprint(ctrl_cves)
    app.register_blueprint(ctrl_index)
    app.register_blueprint(ctrl_image)
    app.register_blueprint(ctrl_images)
    app.register_blueprint(ctrl_image_build)
    app.register_blueprint(ctrl_image_builds)
    app.register_blueprint(ctrl_options)
    app.register_blueprint(ctrl_submit_report)
    app.register_blueprint(ctrl_software)
    app.register_blueprint(ctrl_softwares)
    return True


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    response = e.get_response()
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


app = Flask(__name__)
app.config.update(DEBUG=True)
register_blueprints(app)
glow.db = db.connect()
# glow.options = Options().load_options()

# Development Runner
if __name__ == "__main__":
    logging.info("Starting develop webserver")
    app.run(host='0.0.0.0', port=5001)


# Production Runner
if __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.debug")
    logging.info("Starting production webserver")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# End File: cver/src/cver/api/app.py
