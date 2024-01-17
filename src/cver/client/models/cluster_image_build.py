"""
    Cver Client
    Model
    Cluster Image Build

"""
from cver.shared.models.cluster_image_build import FIELD_MAP
from cver.client.models.base import Base


class ClusterImageBuild(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ClusterImageBuild, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster-image-build"
        self.setup()

# End File: cver/src/cver_client/models/cluster_image_build.py
