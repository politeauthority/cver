"""
    Cver Api
    Collection - Roles

"""
from cver.api.collects.base import Base
from cver.api.models.role import Role


class Roles(Base):

    collection_name = "roles"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Roles, self).__init__(conn, cursor)
        self.table_name = Role().table_name
        self.collect_model = Role
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/roles.py
