"""
    Cver Shared
    Model - Image

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
    "name": {
        "name": "name",
        "type": "str",
        "extra": "UNIQUE"
    },
    "repository": {
        "name": "repository",
        "type": "str",
        "extra": "NOT NULL"
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True
    }
}

# End File: cver/src/shared/models/image.py
