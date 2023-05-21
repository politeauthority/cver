"""
    Cver Api
    Model - ApiKey

"""
from cver.shared.models.api_key import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ApiKey(BaseEntityMeta):

    model_name = "api_key"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(ApiKey, self).__init__(conn, cursor)
        self.table_name = "api_keys"
        self.field_map = FIELD_MAP
        self.setup()

    def get_by_client_id(self, client_id: str):
        """Get an ApiKey by it's client_id."""
        return self.get_by_field("client_id", client_id)

# End File: cver/src/api/models/api_key.py
