"""
    Cver Client
    Collections - ImageBuildWaitings

"""
from cver.shared.models.image_build_waiting import FIELD_MAP
from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


class ImageBuildWaitings(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ImageBuildWaitings, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-waiting"
        self.collection_name = "image-build-waitings"

    def get(self):
        """Get a paginated list of entities."""
        response = self.make_request(self.collection_name)
        if response["status"] == "success":
            return self.build(response["object"])
        else:
            return False

# End File: cver/src/cver_client/collections/image_build_waitings.py
