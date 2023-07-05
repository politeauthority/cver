"""
    Cver Shared
    Model - Role

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
        "api_writeable": True,
    },
    "slug_name": {
        "name": "slug_name",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    }
}

# End File: cver/src/shared/models/role.py
