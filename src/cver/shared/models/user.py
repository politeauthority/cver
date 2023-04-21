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
    "email": {
        "name": "email",
        "type": "str",
        "extra": "UNIQUE",
    },
    "last_login": {
        "name": "last_login",
        "type": "datetime",
    },
    "password": {
        "name": "password",
        "type": "str",
    },
}

# End File: cver/src/shared/modles/fields/user.py
