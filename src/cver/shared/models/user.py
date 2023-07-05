"""
    Cver Shared Model
    Fields User

"""

FIELD_MAP = {
    "id": {
        'name': 'id',
        'type': 'int',
        'primary': True,
    },
    "created_ts": {
        'name': 'created_ts',
        'type': 'datetime',
    },
    "updated_ts": {
        'name': 'updated_ts',
        'type': 'datetime',
    },
    "name": {
        "name": "name",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True,
        "api_searchable": True
    },
    "email": {
        "name": "email",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True,
        "api_searchable": True
    },
    "role_id": {
        "name": "role_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "last_access": {
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True
    }
}

# End File: cver/src/shared/modles/fields/user.py
