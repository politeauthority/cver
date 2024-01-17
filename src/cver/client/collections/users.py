"""
    Cver Client
    Collections - Users

"""
from cver.shared.models.user import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Users(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Users, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "user"
        self.collection_name = "users"


# End File: cver/src/cver_client/collections/users.py
