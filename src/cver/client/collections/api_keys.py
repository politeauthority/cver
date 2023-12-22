"""
    Cver Client
    Collections
    ApiKeys

"""

from cver.shared.models.api_key import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ApiKeys(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ApiKeys, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "api-key"
        self.collection_name = "api-keys"

# End File: cver/src/client/collections/api_keys.py
