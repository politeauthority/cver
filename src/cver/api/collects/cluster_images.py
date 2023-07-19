"""
    Cver Api
    Collects - Images

"""
from cver.api.collects.base import Base
from cver.api.models.cluster_image import ClusterImage


class ClusterImages(Base):

    collection_name = "cluster-images"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ClusterImages, self).__init__(conn, cursor)
        self.table_name = ClusterImage().table_name
        self.collect_model = ClusterImage
        self.per_page = 20

# End File: cver/src/api/collects/cluster_images.py
