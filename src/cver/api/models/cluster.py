"""
    Cver Api
    Model - Cluster

"""
from cver.shared.models.cluster import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class Cluster(BaseEntityMeta):

    model_name = "cluster"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(Cluster, self).__init__(conn, cursor)
        self.table_name = "clusters"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()


# End File: cver/src/api/models/cluster.py
