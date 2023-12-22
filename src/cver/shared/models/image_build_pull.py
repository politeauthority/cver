"""
    Cver Shared
    Model
    Image Build Pull

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
        "api_searchable": True,
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "api_searchable": True,
        "api_writeable": True
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "registry_id": {
        "name": "registry_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True
    },
    "task_id": {
        "name": "task_id",
        "type": "int",
        "extra": "NOT NULL",
        "api_writeable": True,
        "api_searchable": True
    },
    "job": {
        "name": "job",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "status": {
        "name": "status",
        "type": "bool",
        "api_writeable": True,
        "api_searchable": True
    },
    "status_reason": {
        "name": "status_reason",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True
    },
    "pull_time_elapsed": {
        "name": "pull_time_elapsed",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
    "push_time_elapsed": {
        "name": "push_time_elapsed",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True
    },
}

# End File: cver/src/shared/models/image_build_pull.py
