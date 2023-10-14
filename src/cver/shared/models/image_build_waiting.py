"""
    Cver Shared
    Model - ImageBuildWaiting

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
        "api_writeable": True,
        "api_searchable": True,
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "sha": {
        "name": "sha",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "tag": {
        "name": "tag",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "waiting": {
        "name": "waiting",
        "type": "bool",
        "default": True,
        "api_writeable": True,
        "api_searchable": True,
    },
    "waiting_for": {
        "name": "waiting_for",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "status": {
        "name": "status",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True,
    },
    "status_ts": {
        "name": "status_ts",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True,
    },
    "status_reason": {
        "name": "status_reason",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "fail_count": {
        "name": "fail_count",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
}

FIELD_META = {
    "unique_key": ["image_id", "image_build_id"]
}

# End File: cver/src/shared/models/image_build_waiting.py
