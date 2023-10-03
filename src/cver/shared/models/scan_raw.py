"""
    Cver Shared
    Model - Scan Raw

"""

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "user_id": {
        "name": "user_id",
        "type": "int",
        "api_writeable": True,
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "api_writeable": True,
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "api_writeable": True,
    },
    "scanner_id": {
        "name": "scanner_id",
        "type": "int",
        "api_writeable": True,
    },
    "scan_id": {
        "name": "scan_id",
        "type": "int",
        "api_writeable": True,
    },
    "raw": {
        "name": "raw",
        "type": "json",
        "api_writeable": True,
    }
}

# End File: cver/src/shared/models/scan.py
