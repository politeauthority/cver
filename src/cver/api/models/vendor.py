"""Application Model

"""
from .base import Base

FIELD_MAP = [
    {
        'name': 'name',
        'type': 'str',
        "extra": "UNIQUE"
    },
    {
        "name": "slug_name",
        "type": "str",
    }
]

class Vendor(Base):

    model_name = "vendor"

    def __init__(self, conn=None, cursor=None):
        """Create the Vendor instance."""
        super(Vendor, self).__init__(conn, cursor)
        self.table_name = "vendors"
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/modles/vendor.py
