"""
    Cver Client
    Collections - Clusters

"""
from cver.shared.models.cluster import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Clusters(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Clusters, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster"
        self.collection_name = "clusters"

# End File: cver/src/client/collections/clusters.py
