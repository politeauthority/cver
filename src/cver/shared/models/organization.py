"""
    Cver Shared Model
    Organization

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
    "last_access": {
        "name": "last_access",
        "type": "datetime",
        "api_searchable": True
    }
}

# End File: cver/src/shared/models/organization.py
