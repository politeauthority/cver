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
    "type": {
        "name": "type",
        "type": "str",
    },
    "name": {
        "name": "name",
        "type": "str",
        "extra": "UNIQUE",
        "api_searchable": True,
        "api_writeable": True
    },
    "value": {
        "name": "value",
        "type": "str",
        "api_writeable": True
    },
    "acl_write": {
        "name": "acl_write",
        "type": "list",
        "default": ["write-all"],
        "api_writeable": True
    },
    "acl_read": {
        "name": "acl_read",
        "type": "list",
        "default": ["read-all"],
        "api_writeable": True
    },
    "hide_value": {
        "name": "hide_value",
        "type": "bool",
        "api_writeable": True
    }
}

# End File: cver/src/shared/models/fields/option.py
