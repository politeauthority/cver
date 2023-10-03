"""
    Cver Client
    Model
    Scan Raw

"""
from cver.shared.models.scan_raw import FIELD_MAP
from cver.cver_client.models.base import Base


class ScanRaw(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ScanRaw, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "scan-raw"
        self.setup()

# End File: cver/src/cver_client/models/scan_raw.py
