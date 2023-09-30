"""
    Cver Api - Collection
    Scans

"""
from cver.api.collects.base import Base
from cver.api.models.scan import Scan


class Scans(Base):

    collection_name = "scans"

    def __init__(self, conn=None, cursor=None):
        super(Scans, self).__init__(conn, cursor)
        self.table_name = Scan().table_name
        self.collect_model = Scan
        self.per_page = 20

# End File: cve/src/api/collects/scans.py
