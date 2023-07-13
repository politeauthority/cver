"""
    Cver Api
    Model - Migration

"""
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.shared.models.migrate import FIELD_MAP


class Migration(BaseEntityMeta):

    model_name = "migration"

    def __init__(self, conn=None, cursor=None):
        super(Migration, self).__init__(conn, cursor)
        self.table_name = "migrations"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/modles/migration.py
