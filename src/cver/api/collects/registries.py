"""
    Cver Api
    Collection
    Registries

"""
from cver.api.collects.base import Base
from cver.api.models.registry import Registry


class Registries(Base):

    collection_name = "registries"

    def __init__(self, conn=None, cursor=None):
        super(Registries, self).__init__(conn, cursor)
        self.table_name = Registry().table_name
        self.collect_model = Registry
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/registries.py
