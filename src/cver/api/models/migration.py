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

    def get_last(self):
        """Get the last migration."""
        sql = """
        SELECT * FROM `migrations` ORDER BY `id` LIMIT 1;
        """
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        # import ipdb; ipdb.set_trace()
        if not raw:
            return False

        return self.build_from_list(raw)

# End File: cver/src/api/modles/migration.py
