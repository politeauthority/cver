""" 
    Cver Shared Model 
    Fields Software Container Registry

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
    "software_id": {
        "name": "software_id",
        "type": "int",
    },
    "url": {
        "name": "url",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    }
}


# End File: cver/src/shared/modles/fields/software_container_registry.py
