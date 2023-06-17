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
    "image_id": {
        "name": "image_id",
        "type": "int",
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int"
    },
    "scanner_id": {
        "name": "scanner_id",
        "type": "int"
    },
    "scan_id": {
        "name": "scan_id",
        "type": "int"
    },
    "raw": {
        "name": "raw",
        "type": "json"
    }
}

# End File: cver/src/shared/models/scan.py
