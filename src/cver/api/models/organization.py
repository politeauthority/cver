"""
    Cver Api
    Model
    Organization

"""
from cver.shared.models.organization import FIELD_MAP
from cver.api.models.base import Base
from cver.api.utils import sql_tools


class Organization(Base):

    model_name = "organization"

    def __init__(self, conn=None, cursor=None):
        """Create the Orangization instance."""
        super(Organization, self).__init__(conn, cursor)
        self.table_name = "organizations"
        self.field_map = FIELD_MAP
        self.createable = False
        self.setup()

    def __repr__(self):
        """Organization model representation."""
        if self.id and not self.name:
            return "<Org %s>" % self.id
        if self.name and self.id:
            return "<Org: %s %s>" % (self.id, self.name)
        return "<Org>"

    def get_by_email(self, email: str) -> bool:
        sql = """
            SELECT *
            FROM `%(table)s`
            WHERE
                `email`="%(email)s"
            LIMIT 1; """ % {
            "table": self.table_name,
            "email": sql_tools.sql_safe(email)
        }
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/models/organization.py
