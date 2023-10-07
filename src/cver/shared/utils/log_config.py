"""

"""
import os

LOG_LEVEL = os.environ.get("CVER_LOG_LEVEL", "DEBUG")

log_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(module)s: %(message)s",
            "datefmt": "%m-%d %H:%M:%S"
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
    },
    "requests": {
        "level": "warning"
    }
}

# End File: cver/src/cver/shared/utils/log_config.py
