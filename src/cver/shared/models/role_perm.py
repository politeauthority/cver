"""
    Cver Shared
    Model - RolePerm

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
    "role_id": {
        "name": "role_id",
        "type": "int",
    },
    "perm_id": {
        "name": "perm_id",
        "type": "int",
    },
    "enabled": {
        "name": "enabled",
        "type": "bool",
        "default": True
    }
}

# End File: cver/src/shared/models/role_perm.py
