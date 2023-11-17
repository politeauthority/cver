"""
    Cver Api
    Collections
    Organizations

"""
from cver.api.collects.base import Base
from cver.api.models.organization import Organization


class Organizations(Base):

    collection_name = "organizations"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Organizations, self).__init__(conn, cursor)
        self.table_name = Organization().table_name
        self.collect_model = Organization
        self.field_map = self.collect_model().field_map


# End File: cver/src/api/collects/organizations.py
