"""
    Cver Client
    Model - User

"""
from cver.shared.models.image import FIELD_MAP
from cver.cver_client.models.base import Base


class User(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(User, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "user"
        self.setup()


# End File: cver/src/cver_client/models/user.py
