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
        "extra": "UNIQUE",
        "api_writeable": True,
        "api_searchable": True,
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "repository": {
        "name": "repository",
        "type": "str",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "tags": {
        "name": "tags",
        "type": "list",
        "api_writeable": True
    },
    "os_family": {
        "name": "os_family",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True
    },
    "os_name": {
        "name": "os_name",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True,
        "api_writeable": True
    },
    "scan_flag": {
        "name": "scan_flag",
        "type": "bool",
        "api_writeable": True
    },
    "scan_enabled": {
        "name": "scan_enabled",
        "type": "bool",
        "default": True,
        "api_writeable": True
    },
    "scan_last_ts": {
        "name": "scan_last_ts",
        "type": "datetime",
        "api_writeable": True
    },
    "pending_operation": {
        "name": "pending_operation",
        "type": "str",
        "api_writeable": True
    },
}

# End File: cver/src/shared/models/image_build.py
