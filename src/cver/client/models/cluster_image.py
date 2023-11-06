"""
    Cver Client
    Model - ClusterImage

"""
from cver.shared.models.cluster_image import FIELD_MAP
from cver.client.models.base import Base


class ClusterImage(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ClusterImage, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "cluster_iamge"
        self.setup()

# End File: cver/src/cver_client/models/cluster_image.py
