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
    "sha_imported": {
        "name": "sha_imported",
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
    "registry": {
        "name": "registry",
        "type": "str",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "registry_imported": {
        "name": "registry_imported",
        "type": "str",
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
        "api_writeable": True,
        "api_searchable": True,
    },
    "sync_flag": {
        "name": "sync_flag",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
    "sync_enabled": {
        "name": "sync_enabled",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
    "sync_last_ts": {
        "name": "sync_last_ts",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_flag": {
        "name": "scan_flag",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_enabled": {
        "name": "scan_enabled",
        "type": "bool",
        "default": True,
        "api_writeable": True,
        "api_searchable": True
    },
    "scan_last_ts": {
        "name": "scan_last_ts",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True
    }
}

# End File: cver/src/shared/models/image_build.py
