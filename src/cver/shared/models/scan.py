"""
    Cver Shared
    Model - Scan

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
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
        "api_searchable": True,
        "api_writeable": True,
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int",
        "api_searchable": True,
        "api_writeable": True,
    },
    "scanner_id": {
        "name": "scanner_id",
        "type": "int",
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_critical_int": {
        "name": "cve_critical_int",
        "type": "int",
        "default": 0,
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_critical_nums": {
        "name": "cve_critical_nums",
        "type": "list",
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_high_int": {
        "name": "cve_high_int",
        "type": "int",
        "default": 0,
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_high_nums": {
        "name": "cve_high_nums",
        "type": "list",
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_medium_int": {
        "name": "cve_medium_int",
        "type": "int",
        "default": 0,
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_medium_nums": {
        "name": "cve_medium_nums",
        "type": "list",
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_low_int": {
        "name": "cve_low_int",
        "type": "int",
        "default": 0,
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_low_nums": {
        "name": "cve_low_nums",
        "type": "list",
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_unknown_int": {
        "name": "cve_unknown_int",
        "type": "int",
        "default": 0,
        "api_searchable": True,
        "api_writeable": True,
    },
    "cve_unknown_nums": {
        "name": "cve_unknown_nums",
        "type": "list",
        "api_searchable": True,
        "api_writeable": True,
    },
    "pending_parse": {
        "name": "pending_parse",
        "type": "bool",
        "api_writeable": True,
    }
}

# End File: cver/src/shared/models/scan.py
