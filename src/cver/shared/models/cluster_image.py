"""
    Cver Shared
    Model - ClusterImage

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
    "image_id": {
        "name": "image_id",
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
    },
    "last_seen": {
        "name": "last_seen",
        "type": "datetime",
    },

}

# End File: cver/src/shared/models/cluster_image.py
