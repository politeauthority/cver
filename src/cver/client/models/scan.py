"""
    Cver Client
    Model
    Scan

"""
from cver.shared.models.scan import FIELD_MAP
from cver.client.models.base import Base


class Scan(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Scan, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "scan"
        self.setup()

# End File: cver/src/cver_client/models/scan.py
