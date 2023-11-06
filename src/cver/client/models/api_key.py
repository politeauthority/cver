"""
    Cver Client
    Model - ApiKey

"""
from cver.shared.models.api_key import FIELD_MAP
from cver.client.models.base import Base


class ApiKey(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ApiKey, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "api-key"
        self.setup()

# End File: cver/src/cver_client/models/api_key.py
