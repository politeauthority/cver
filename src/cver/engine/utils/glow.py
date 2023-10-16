"""
    Cver Engine
    Glow
    Global variables for Cver Engine.
"""

global registry_info

registry_info = {
    "local": {
        "url": None,
        "user": None,
        "pass": None
    },
    "pull_thrus": {
        "docker.io": "cver-docker-hub",
        "quay.io": "cver-quay",
        "ghcr.io": "cver-ghcr"
    }
}

# End File: cver/src/engine/utils/glow.py
