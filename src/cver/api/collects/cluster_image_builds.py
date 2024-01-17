"""
    Cver Api
    Collects
    Cluster Image Builds

"""
from cver.api.collects.base import Base
from cver.api.models.cluster_image_build import ClusterImageBuild


class ClusterImageBuilds(Base):

    collection_name = "cluster-image-builds"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ClusterImageBuilds, self).__init__(conn, cursor)
        self.table_name = ClusterImageBuild().table_name
        self.collect_model = ClusterImageBuild
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cver/src/api/collects/cluster_image_builds.py
