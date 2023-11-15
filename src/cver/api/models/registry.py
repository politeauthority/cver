"""
    Cver Api
    Model
    Registry

"""
from cver.shared.models.registry import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class Registry(BaseEntityMeta):

    model_name = "registry"

    def __init__(self, conn=None, cursor=None):
        """Create the Registry instance."""
        super(Registry, self).__init__(conn, cursor)
        self.table_name = "image_builds"
        self.field_map = FIELD_MAP
        self.createable = True
        self.insert_iodku = False
        self.setup()

# End File: cver/src/api/models/registry.py
