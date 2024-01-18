"""
    Cver Shared
    Model - ApiKey

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
    "user_id": {
        "name": "user_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "client_id": {
        "name": "client_id",
        "type": "str",
        "extra": "UNIQUE",
        "api_searchable": True,
    },
    "key": {
        "name": "key",
        "type": "str",
        "api_display": False
    },
    "last_access": {
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True,
    },
    "last_ip": {
        "name": "last_ip",
        "type": "str",
        "api_searchable": True,
    },
    "expiration_date": {
        "name": "expiration_date",
        "type": "datetime",
        "api_searchable": True,
    },
    "enabled": {
        "name": "enabled",
        "type": "bool",
        "default": True,
        "api_searchable": True,
    }
}

# End File: cver/src/shared/models/api_key.py
