"""
    Cver Shared
    Model
    Cluster Image Build

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
        "api_writeable": True,
        "api_searchable": True,
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True,
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "cluster_id": {
        "name": "cluster_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True,
    },
    "first_seen": {
        "name": "first_seen",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True,
    },
    "last_seen": {
        "name": "last_seen",
        "type": "datetime",
        "api_writeable": True,
        "api_searchable": True,
    },
    "present": {
        "name": "present",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True,
    },
}

FIELD_META = {
    "unique_key": ["image_build_id", "cluster_id"]
}


# End File: cver/src/shared/models/cluster_image_build.py
