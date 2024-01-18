"""
    Cver Client
    Collections
    Cluster Images

"""
from cver.shared.models.cluster_image import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ClusterImages(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ClusterImages, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster-image"
        self.collection_name = "cluster-images"

# End File: cver/src/client/collections/cluster_images.py
