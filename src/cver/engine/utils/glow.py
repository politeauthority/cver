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

global engine_info
engine_info = {
    "download_limit": 0,
    "scan_limit": 0 
}

# End File: cver/src/engine/utils/glow.py
