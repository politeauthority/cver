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
    },
    "email": {
        "name": "email",
        "type": "str",
        "extra": "UNIQUE",
    },
    "role_id": {
        "name": "role_id",
        "type": "int",
    },
    "last_access": {
        "name": "last_access",
        "type": "datetime",
    },
    "password": {
        "name": "password",
        "type": "str",
    },
}

# End File: cver/src/shared/modles/fields/user.py
