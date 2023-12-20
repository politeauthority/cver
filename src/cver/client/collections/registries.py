"""
    Cver Client
    Collections
    Registries

"""
from cver.shared.models.registry import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Registries(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Registries, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "registry"
        self.collection_name = "registries"


# End File: cver/src/client/collections/registries.py
