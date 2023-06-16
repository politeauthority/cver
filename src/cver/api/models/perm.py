"""
    Cver Api
    Model - Perm

"""
from cver.shared.models.perm import FIELD_MAP
from cver.shared.utils import xlate
from cver.api.models.base_entity_meta import BaseEntityMeta


class Perm(BaseEntityMeta):

    model_name = "perm"

    def __init__(self, conn=None, cursor=None):
        """Create the Perm instance."""
        super(Perm, self).__init__(conn, cursor)
        self.table_name = "perms"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Perm %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Perm>"

    def get_by_slug(self, slug_name: str) -> bool:
        sql = """
            SELECT *
            FROM `perms`
            WHERE
                `slug_name` = "%s"
            LIMIT 1; """ % xlate.sql_safe(slug_name)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True


# End File: cver/src/api/modles/perm.py
