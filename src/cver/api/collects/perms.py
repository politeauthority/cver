"""
    Cver Api
    Collection - RolePerm

"""
from cver.api.collects.base import Base
from cver.api.models.perm import Perm


class Perms(Base):

    collection_name = "role_perms"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Perms, self).__init__(conn, cursor)
        self.table_name = Perm().table_name
        self.collect_model = Perm
        self.per_page = 20

# End File: cve/src/api/collects/perms.py