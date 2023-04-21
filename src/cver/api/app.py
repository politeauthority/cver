#!/usr/bin/env python
"""Cver Api App

"""
from flask import Flask, jsonify

from cver.api.utils import db
from cver.api.utils import glow
from cver.api.controllers.ctrl_collections.ctrl_options import ctrl_options
from cver.api.controllers.ctrl_collections.ctrl_softwares import ctrl_softwares
from cver.api.controllers.ctrl_models.ctrl_software import ctrl_software


app = Flask(__name__)
app.config.update(DEBUG=True)


def register_blueprints(app: Flask) -> bool:
    """Register controller blueprints to flask."""
    # app.register_blueprint(ctrl_cves)
    app.register_blueprint(ctrl_options)
    app.register_blueprint(ctrl_software)
    app.register_blueprint(ctrl_softwares)
    return True


@app.route('/')
def index():
    data = {
        "info": "Cver Api",
        "version": "0.0.1"
    }
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify(data)


@app.route('/debug')
def debug():
    data = {
        "debug": "Hello",
        "info": "Cver Api",
        "version": "0.0.1",
        "build": "beta"
    }
    return jsonify(data)


if __name__ == "__main__":
    glow.db = db.connect()
    # glow.options = Options().load_options()
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5001)

# End File: cver/src/api/app.py
