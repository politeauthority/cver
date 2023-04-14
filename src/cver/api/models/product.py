"""CVSS -  Model

"""
from .base import Base

FIELD_MAP = [
    {
        'name': 'name',
        'type': 'str',
        "extra": "UNIQUE"
    },
    {
        "name": "vendor_id",
        "type": "int",
        "default": None,
    },
    {
        "name": "",
        "type": "int",
        "default": None,
    }
]


class Product(Base):

    model_name = "prodcut"

    def __init__(self, conn=None, cursor=None):
        """Create the Product instance."""
        super(Product, self).__init__(conn, cursor)
        self.table_name = "products"
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/modles/product.py
