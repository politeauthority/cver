"""
    Cver Api - Collection
    Api Keys

"""
from cver.api.collects.base import Base
from cver.api.models.api_key import ApiKey


class ApiKeys(Base):
    """Collection class for gathering groups of device macs."""

    collection_name = "api_keys"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ApiKeys, self).__init__(conn, cursor)
        self.table_name = ApiKey().table_name
        self.collect_model = ApiKey
        self.per_page = 20

# End File: cve/src/api/collects/api_keys.py
