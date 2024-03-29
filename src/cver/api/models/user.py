"""
    Cver Api
    Model
    User

"""
from cver.shared.models.user import FIELD_MAP
from cver.api.models.base import Base
from cver.api.utils import sql_tools


class User(Base):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance."""
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def __repr__(self):
        """User model representation."""
        if self.id and not self.name:
            return "<User %s>" % self.id
        if self.name and self.id:
            return "<User: %s %s>" % (self.id, self.name)
        return "<User>"

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
