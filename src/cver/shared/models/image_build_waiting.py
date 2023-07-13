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
}

# End File: cver/src/shared/models/image_build_waiting.py