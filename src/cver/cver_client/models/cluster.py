"""
    Cver Client
    Model - Cluster

"""
from cver.shared.models.cluster import FIELD_MAP
from cver.cver_client.models.base import Base


class Cluster(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Cluster, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster"
        self.setup()

# End File: cver/src/cver_client/models/cluster.py
