"""
    Cver Client
    Collections
    ImageBuilds

"""

from cver.shared.models.image_build_waiting import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ImageBuilds(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ImageBuilds, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build"
        self.collection_name = "image-builds"

    def get_by_image_id(self, image_id: int, page: int = 1) -> list:
        """Get a list of ImageBuilds by an Image ID."""
        payload = {
            "image_id": image_id
        }
        return self.get(payload, page)

# End File: cver/src/client/collections/image_builds.py
