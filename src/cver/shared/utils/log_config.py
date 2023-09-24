"""

"""
import os

LOG_LEVEL = os.environ.get("CVER_LOG_LEVEL")

log_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(module)s: %(message)s",
        }
    },
    "handlers": {
        "wsgi": {
            "class": "logging.StreamHandler",
            "stream": "ext://flask.logging.wsgi_errors_stream",
            "formatter": "default"
        }
    },
    "root": {
        "level": LOG_LEVEL,
        "handlers": ["wsgi"]
    }
}

# End File: cver/src/cver/shared/utils/log_config.py
