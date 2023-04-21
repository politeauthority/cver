"""Cver Shared - Model Cvss

"""
from cver.api.models.base import Base

FIELD_MAP = [
    {
        "name": "cve_id",
        "type": "int",
        "extra": "UNIQUE"
    },
    {
        "name": "cve_number",
        "type": "str",
    },
    {
        "name": "source",
        "type": "str",
    },
    {
        "name": "published",
        "type": "datetime",
    },
    {
        "name": "last_modified",
        "type": "datetime",
    },
    {
        "name": "vuln_status",
        "type": "str",
    },
    {
        "name": "type",
        "type": "str",
    },
    {
        "name": "base_severity",
        "type": "str",
    },
    {
        "name": "exploitability_score",
        "type": "float",
    },

    {
        "name": "impact_score",
        "type": "float",
    },
    {
        "name": "ac_insuf_info",
        "type": "str",
    },
    {
        "name": "obtain_all_privilege",
        "type": "str",
    },
    {
        "name": "obtain_user_privilege",
        "type": "bool",
    },
    {
        "name": "user_interaction_required",
        "type": "bool",
    }
]


class Cvss(Base):

    model_name = "cvss"

    def __init__(self, conn=None, cursor=None):
        """Create the Cvss instance."""
        super(Cvss, self).__init__(conn, cursor)
        self.table_name = "cvss"
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/shared/modles/cvss.py
