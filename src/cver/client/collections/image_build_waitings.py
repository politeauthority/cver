"""
    Cver Client
    Collections
    ImageBuildWaitings

"""

from cver.shared.models.image_build_waiting import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ImageBuildWaitings(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ImageBuildWaitings, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-waiting"
        self.collection_name = "image-build-waitings"

    def get_by_image_id(self, image_id: int, page: int = 1) -> list:
        """Get a list of ImageBuildWaitings by an Image ID."""
        payload = {
            "image_id": image_id
        }
        return self.get(payload, page)

# End File: cver/src/client/collections/image_build_waitings.py
