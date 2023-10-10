"""
    Cver Shared
    Model
    Task

"""

FIELD_MAP = {
    "id": {
        "name": "id",
        "type": "int",
        "primary": True,
    },
    "created_ts": {
        "name": "created_ts",
        "type": "datetime",
    },
    "updated_ts": {
        "name": "updated_ts",
        "type": "datetime",
    },
    "user_id": {
        "name": "user_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "name": {
        "name": "name",
        "type": "str",
        "api_writeable": True,
        "api_searchable": True,
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
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
    "image_build_waiting_id": {
        "name": "image_build_waiting_id",
        "type": "int",
        "api_writeable": True,
        "api_searchable": True,
    },
    "status": {
        "name": "status",
        "type": "bool",
        "api_writeable": True
    },
    "status_reason": {
        "name": "status_reason",
        "type": "str",
        "api_writeable": True
    },
    "start_ts": {
        "name": "start_ts",
        "type": "datetime",
        "api_writeable": True
    },
    "end_ts": {
        "name": "end_ts",
        "type": "datetime",
        "api_writeable": True
    },
}

# End File: cver/src/shared/models/task.py
