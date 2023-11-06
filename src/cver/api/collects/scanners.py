"""
    Cver Api - Collection
    Scanners

"""
from cver.api.collects.base import Base
from cver.api.models.scanner import Scanner


class Scanners(Base):

    collection_name = "scanners"

    def __init__(self, conn=None, cursor=None):
        super(Scanners, self).__init__(conn, cursor)
        self.table_name = Scanner().table_name
        self.collect_model = Scanner
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/scanners.py
