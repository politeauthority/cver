"""User - Model

"""
from .base import Base

FIELD_MAP = [
    {
        'name': 'email',
        'type': 'str',
        "extra": "UNIQUE"
    },
    {
        "name": "last_login",
        "type": "datetime",
    },
    {
        "name": "password",
        "type": "str",
    }
]

class User(Base):

    model_name = "user"

    def __init__(self, conn=None, cursor=None):
        """Create the User instance."""
        super(User, self).__init__(conn, cursor)
        self.table_name = "users"
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/modles/user.py
