"""
    Cver Api
    Collection - RolePerm

"""
from cver.api.collects.base import Base
from cver.api.models.role_perm import RolePerm


class RolePerms(Base):

    collection_name = "role_perms"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(RolePerms, self).__init__(conn, cursor)
        self.table_name = RolePerm().table_name
        self.collect_model = RolePerm
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/role_perms.py
