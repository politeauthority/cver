"""
    Cver Shared
    Model
    Image Sync

"""

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
        "api_searchable": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
        "api_searchable": True,
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
        "api_searchable": True,
    },
    "registry_id": {
        "name": "name",
        "type": "registry_id",
        "extra": "NOT NULL",
        "api_searchable": True,
        "api_writeable": True
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True
    },
    "local_url": {
        "name": "local_url",
        "type": "str",
        "default": True,
        "api_writeable": True,
        "api_searchable": True
    },
    "success_download": {
        "name": "success_download",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
    "success_push": {
        "name": "success_push",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
}

# End File: cver/src/shared/models/image_sync.py
