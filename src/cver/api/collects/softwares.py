"""Cves Collection.
Gets collection of Cves

"""
from cver.api.collects.base import Base
from cver.api.models.software import Software


class Softwares(Base):

    collection_name = "softwares"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Softwares, self).__init__(conn, cursor)
        self.table_name = Software().table_name
        self.collect_model = Software
        self.per_page = 20

# End File: cve/src/api/collects/softwares.py
