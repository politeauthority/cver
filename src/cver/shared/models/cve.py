""" Cver Shared Model Fields Cve

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
    "number": {
        "name": "number",
        "type": "str",
        "extra": "UNIQUE"
    },
    "published": {
        "name": "published",
        "type": "datetime",
        "default": None,
    },
}


# End File: cver/src/shared/modles/fields/cve.py
