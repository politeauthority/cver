"""
    Cver Api - Collection
    Scan Raws

"""
from cver.api.collects.base import Base
from cver.api.models.scan_raw import ScanRaw


class ScanRaws(Base):

    collection_name = "scan_raws"

    def __init__(self, conn=None, cursor=None):
        super(ScanRaws, self).__init__(conn, cursor)
        self.table_name = ScanRaw().table_name
        self.collect_model = ScanRaw
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/scan_raws.py
