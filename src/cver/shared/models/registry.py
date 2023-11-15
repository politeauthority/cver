"""
    Cver Shared
    Model
    Registry

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
    "url": {
        "name": "url",
        "type": "str",
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
    },
    "daily_limit": {
        "name": "daily_limit",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "public": {
        "name": "public",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
}

# End File: cver/src/shared/models/registry.py
