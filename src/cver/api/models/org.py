"""
    Cver Api
    Model - Org

"""
from cver.shared.models.org import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class Org(BaseEntityMeta):

    model_name = "org"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(Org, self).__init__(conn, cursor)
        self.table_name = "orgs"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()


# End File: cver/src/api/modles/orgs.py
