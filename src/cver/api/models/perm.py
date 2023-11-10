"""
    Cver Api
    Model - Perm

"""
from cver.shared.models.perm import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.api.utils import sql_tools


class Perm(BaseEntityMeta):

    model_name = "perm"

    def __init__(self, conn=None, cursor=None):
        """Create the Perm instance.
        :unit-test: TestApiModelPerm::test____init__
        """
        super(Perm, self).__init__(conn, cursor)
        self.table_name = "perms"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def __repr__(self):
        """
        :unit-test: TestApiModelPerm::test____repr__
        """
        if self.id:
            return "<Perm %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Perm>"

    def get_by_slug(self, slug_name: str) -> bool:
        """Get a permission by it's slug name.
        :unit-test: TestApiModelPerm::test__get_by_slug
        """
        sql = """
            SELECT *
            FROM `perms`
            WHERE
                `slug_name` = "%s"
            LIMIT 1; """ % sql_tools.sql_safe(slug_name)
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True


# End File: cver/src/api/models/perm.py
