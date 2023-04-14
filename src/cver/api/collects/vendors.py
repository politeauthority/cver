"""Cves Collection.
Gets collection of Cves

"""
from cver.api.utils import xlate
from cver.api.collects.base import Base
from cver.api.models.vendor import Vendor


class Vendors(Base):
    """Collection class for gathering groups of device macs."""

    collection_name = "vendors"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Vendors, self).__init__(conn, cursor)
        self.table_name = Vendor().table_name
        self.collect_model = Vendor
        self.per_page = 20

# End File: cve/src/api/collections/vendors.py
