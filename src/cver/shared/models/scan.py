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
    },
    "image_id": {
        "name": "image_id",
        "type": "int",
    },
    "image_build_id": {
        "name": "image_build_id",
        "type": "int"
    },
    "scanner_id": {
        "name": "scanner_id",
        "type": "int",
    },
    "cve_critical_int": {
        "name": "cve_critical_int",
        "type": "int",
        "default": 0
    },
    "cve_critical_nums": {
        "name": "cve_critical_nums",
        "type": "list"
    },
    "cve_high_int": {
        "name": "cve_high_int",
        "type": "int",
        "default": 0
    },
    "cve_high_nums": {
        "name": "cve_high_nums",
        "type": "list"
    },
    "cve_medium_int": {
        "name": "cve_medium_int",
        "type": "int",
        "default": 0
    },
    "cve_medium_nums": {
        "name": "cve_medium_nums",
        "type": "list"
    },
    "cve_low_int": {
        "name": "cve_low_int",
        "type": "int",
        "default": 0
    },
    "cve_low_nums": {
        "name": "cve_low_nums",
        "type": "list"
    },
    "cve_unknown_int": {
        "name": "cve_unknown_int",
        "type": "int",
        "default": 0
    },
    "cve_unknown_nums": {
        "name": "cve_unknown_nums",
        "type": "list"
    },
    "pending_parse": {
        "name": "pending_parse",
        "type": "bool"
    }
}

# End File: cver/src/shared/models/scan.py
