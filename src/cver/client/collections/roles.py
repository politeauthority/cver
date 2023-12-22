"""
    Cver Client
    Collections
    Roles

"""
from cver.shared.models.role import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Roles(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Roles, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "role"
        self.collection_name = "roles"


# End File: cver/src/cver_client/collections/roles.py
