"""
    Cver Client
    Collections - Images

"""
from cver.shared.models.image import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Images(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Images, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image"
        self.collection_name = "images"


# End File: cver/src/client/collections/images.py
