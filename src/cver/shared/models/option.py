""" Cver Shared Model
    Fields Option

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
        "name": "number",
        "type": "str",
        "extra": "UNIQUE",
    },
    "value": {
        "name": "value",
        "type": "str",
    },
}

# End File: cver/src/shared/modles/fields/option.py
