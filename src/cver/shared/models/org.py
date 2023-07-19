"""
    Cver Shared
    Model - Org

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
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "name": {
        "name": "name",
        "type": "str",
        "extra": "UNIQUE",
        "api_searchable": True,
        "api_writeable": True
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True,
        "api_writeable": True
    }
}

# End File: cver/src/shared/models/org.py
