"""
    Cver Api
    Collects - Migrations

"""
from cver.api.collects.base import Base
from cver.api.models.migration import Migration


class Migrations(Base):

    collection_name = "migrations"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Migrations, self).__init__(conn, cursor)
        self.table_name = Migration().table_name
        self.collect_model = Migration
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/migrations.py
