"""
    Cver Api
    Model - ApiKey

"""
from cver.shared.models.api_key import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ApiKey(BaseEntityMeta):

    model_name = "api_key"

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ApiKey, self).__init__(conn, cursor)
        self.table_name = "api_keys"
        self.field_map = FIELD_MAP
        self.immutable = True
        self.setup()

    def __repr__(self):
        """ApiKey model representation. """
        if self.id and self.client_id:
            return "<%s: %s-%s>" % (self.__class__.__name__, self.id, self.client_id)
        elif self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

    def get_by_client_id(self, client_id: str):
        """Get an ApiKey by it's client_id."""
        return self.get_by_field("client_id", client_id)

# End File: cver/src/api/models/api_key.py
