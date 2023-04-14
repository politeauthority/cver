""" Cver Shared Model Fields Software

"""

FIELD_MAP = [
    {
        "name": "name",
        "type": "str",
        "api_writeable": True
    },
    {
        "name": "slug_name",
        "type": "str",
        "api_writeable": True
    },
    {
        "name": "url_git",
        "type": "str",
        "extra": "UNIQUE",
        "api_writeable": True
    },
    {
        "name": "url_marketing",
        "type": "str",
        "api_writeable": True
    },
]

# End File: cver/src/shared/modles/fields/software.py
