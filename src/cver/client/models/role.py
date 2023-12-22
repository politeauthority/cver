"""
    Cver Client
    Model
    Role

"""
from cver.shared.models.role import FIELD_MAP
from cver.client.models.base import Base


class Role(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Role, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "role"
        self.setup()

# End File: cver/src/cver_client/models/role.py
