"""
    Cver Shared
    Model - Migrate

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
    "number": {
        "name": "number",
        "type": "int",
    },
    "up_sql": {
        "name": "up_sql",
        "type": "str",
    },
    "down_sql": {
        "name": "down_sql",
        "type": "str",
    },
    "success": {
        "name": "success",
        "type": "bool",
    }
}

# End File: cver/src/shared/models/migrate.py
