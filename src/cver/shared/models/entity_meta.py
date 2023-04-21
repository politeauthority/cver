""" Cver Shared Model 
    Fields EntityMeta

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
    "entity_type": {
        'name': 'entity_type',
        'type': 'str',
    },
    "entity_id": {
        'name': 'entity_id',
        'type': 'int',
    },
    "name": {
        'name': 'name',
        'type': 'str',
    },
    "type": {
        "name": "type",
        "type": "str"
    },
    "value": {
        "name": "value",
        "type": "str"
    },
}

# End File: cver/src/shared/modles/fields/entity_meta.py
