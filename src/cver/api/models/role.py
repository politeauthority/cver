"""
    Cver Api
    Model - Role

"""
from cver.shared.models.role import FIELD_MAP
from cver.api.models.base import Base


class Role(Base):

    model_name = "role"

    def __init__(self, conn=None, cursor=None):
        super(Role, self).__init__(conn, cursor)
        self.table_name = "roles"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def __repr__(self):
        if self.id:
            return "<Role %s:%s>" % (self.id, self.slug_name)
        else:
            return "<Role>"

# End File: cver/src/api/modles/role.py
