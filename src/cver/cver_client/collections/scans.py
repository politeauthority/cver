"""
    Cver Client
    Collections
    Scans

"""
from cver.shared.models.scan import FIELD_MAP
from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


class Scans(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Scans, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "scan"
        self.collection_name = "scans"

    def get_by_image_id(self, image_id: int, page: int = 1) -> list:
        """Get a list of Scans by an Image ID."""
        payload = {
            "image_id": image_id
        }
        return self.get(payload, page)

    def get_by_image_build_id(self, image_build_id: int, page: int = 1) -> list:
        """Get a list of Scans by an ImageBuild ID."""
        payload = {
            "image_build_id": image_build_id
        }
        return self.get(payload, page)

# End File: cver/src/cver_client/collections/scans.py
