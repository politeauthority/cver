"""
    Cver Client
    Collections
    ImageBuildPulls

"""

from cver.shared.models.image_build_pull import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ImageBuildPulls(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ImageBuildPulls, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-pull"
        self.collection_name = "image-build-pulls"

# End File: cver/src/client/collections/image_build_pulls.py
