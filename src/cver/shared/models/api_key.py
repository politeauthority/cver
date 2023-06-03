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
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "user_id": {
        "name": "user_id",
        "type": "int",
        "api_writeable": True
    },
    "client_id": {
        "name": "client_id",
        "type": "str",
        "extra": "UNIQUE",
    },
    "key": {
        "name": "key",
        "type": "str",
        "api_display": False
    },
    "last_access": {
        "name": "last_access",
        "type": "datetime",
    },
    "last_ip": {
        "name": "last_ip",
        "type": "str",
    },
    # "expiration_date": {
    #     "name": "expiration_date",
    #     "type": "datetime",
    #     "api_writeable": True
    # }
}

# End File: cver/src/shared/models/api_key.py
