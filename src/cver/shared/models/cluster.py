"""
    Cver Shared
    Model - Cluster

"""

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
        "api_searchable": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "org_id": {
        "name": "org_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "name": {
        "name": "name",
        "type": "str",
        "api_searchable": True,
        "api_writeable": True
    },
    "maintained": {
        "name": "maintained",
        "type": "bool",
        "default": True,
        "api_writeable": True
    }
}

# End File: cver/src/shared/models/cluster.py
