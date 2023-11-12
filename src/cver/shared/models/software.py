""" Cver Shared -  Model Fields - Software

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
    "slug_name": {
        "name": "slug_name",
        "type": "str",
        "api_writeable": True
    },
    "software_id": {
        "name": "software_id",
        "type": "int",
    },
    "url_git": {
        "name": "url_git",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True
    },
    "url_marketing": {
        "name": "url_marketing",
        "type": "str",
        "api_writeable": True
    }
}


# End File: cver/src/shared/models/fields/software.py
