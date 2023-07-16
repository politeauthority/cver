"""
    Cver Api
    Collects - Clusters

"""
from cver.api.collects.base import Base
from cver.api.models.cluster import Cluster


class Clusters(Base):

    collection_name = "clusters"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Clusters, self).__init__(conn, cursor)
        self.table_name = Cluster().table_name
        self.collect_model = Cluster
        self.per_page = 20

# End File: cver/src/api/collects/cluster.py
