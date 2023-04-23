"""
    Cver Shared
    Model - ImageBuild

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
    "sha": {
        "name": "sha",
        "type": "str",
        "extra": "UNIQUE"
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "extra": "NOT NULL"
    },
    "repository": {
        "name": "repository",
        "type": "str",
        "extra": "NOT NULL"
    },
    "tags": {
        "name": "tags",
        "type": "list"
    },
    "os_family": {
        "name": "os_family",
        "type": "str",
        "extra": "UNIQUE"
    },
    "os_name": {
        "name": "os_name",
        "type": "str",
        "extra": "UNIQUE"
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True
    },
    "scan_flag": {
        "name": "scan_flag",
        "type": "bool"
    },
    "scan_enabled": {
        "name": "scan_enabled",
        "type": "bool",
        "default": True,
    },
    "scan_last_ts": {
        "name": "scan_last_ts",
        "type": "datetime",
    },
    "pending_operation": {
        "name": "pending_operation",
        "type": "str",
    },
}

# End File: cver/src/shared/models/image_build.py
