"""
    Cver Client
    Collections
    Cluster Image Builds

"""
from cver.shared.models.cluster_image_build import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class ClusterImageBuilds(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ClusterImageBuilds, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster-image-build"
        self.collection_name = "cluster-image-builds"

# End File: cver/src/client/collections/cluster_image_builds.py
