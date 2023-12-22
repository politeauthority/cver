"""
    Cver Shared
    Model
    Image

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
    },
    "name": {
        "name": "name",
        "type": "str",
        "extra": "NOT NULL",
        "api_searchable": True,
        "api_writeable": True
    },
    "registry_id": {
        "name": "registry_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True,
        "api_writeable": True,
        "api_searchable": True
    }
}

FIELD_META = {
    "unique_key": ["name", "registry_id"]
}

# End File: cver/src/shared/models/image.py
