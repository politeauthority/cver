"""
    Cver Api
    Model - RolePerm

"""
from cver.shared.models.role import FIELD_MAP
from cver.shared.utils import xlate
from cver.api.models.base import Base


class RolePerm(Base):

    model_name = "role_perm"

    def __init__(self, conn=None, cursor=None):
        super(RolePerm, self).__init__(conn, cursor)
        self.table_name = "role_perms"
        self.field_map = FIELD_MAP
        self.setup()

    def __repr__(self):
        if self.id:
            return "<RolePerm %s:(Role.ID %s, Perm.ID %s)>" % (self.id, self.role_id, self.perm_id)
        else:
            return "<RolePerm %s>" % (self.id)

    def get_by_role_perm(self, role_id: int, perm_id) -> bool:
        sql = """
            SELECT *
            FROM `role_perms`
            WHERE
                `role_id` = %s AND
                `perm_id` = %s AND
                `enabled` = 1
            LIMIT 1; """ % (xlate.sql_safe(role_id), xlate.sql_safe(perm_id))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/modles/role_perm.py
