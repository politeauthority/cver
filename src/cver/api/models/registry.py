"""
    Cver Api
    Model
    Registry

"""
from cver.shared.models.registry import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.api.utils import sql_tools


class Registry(BaseEntityMeta):

    model_name = "registry"

    def __init__(self, conn=None, cursor=None):
        """Create the Registry instance."""
        super(Registry, self).__init__(conn, cursor)
        self.table_name = "registries"
        self.field_map = FIELD_MAP
        self.createable = True
        self.insert_iodku = False
        self.setup()

    def get_by_url(self, registry_url: str) -> bool:
        """Get a Registry entity by it's url."""
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                `url` = "%s";
        """ % (
            self.table_name,
            sql_tools.sql_safe(registry_url))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/models/registry.py
