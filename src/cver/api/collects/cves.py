"""Cves Collection.
Gets collection of Cves

"""
from cver.api.collects.base import Base
from cver.api.models.cve import Cve


class Cves(Base):
    """Collection class for gathering groups of device macs."""

    collection_name = "cves"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Cves, self).__init__(conn, cursor)
        self.table_name = Cve().table_name
        self.collect_model = Cve
        self.per_page = 20

# End File: cve/src/api/collections/cves.py
