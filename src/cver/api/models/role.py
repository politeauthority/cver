"""
    Cver Api
    Model - Role

"""
from cver.shared.models.role import FIELD_MAP
from cver.shared.utils import xlate
from cver.api.models.base import Base


class Role(Base):

    model_name = "role"

    def __init__(self, conn=None, cursor=None):
        super(Role, self).__init__(conn, cursor)
        self.table_name = "roles"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Role %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Role %s>" % (self.slug_name)

    def get_by_slug(self, slug_name: str) -> bool:
        sql = """
            SELECT *
            FROM `roles`
            WHERE
                `slug_name` = "%s"
            LIMIT 1; """ % xlate.sql_safe(slug_name)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/modles/role.py
