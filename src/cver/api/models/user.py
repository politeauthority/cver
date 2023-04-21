"""User - Model

"""
from cver.shared.models.software import FIELD_MAP
from cver.api.models.base import Base


class User(Base):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance."""
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/modles/user.py
