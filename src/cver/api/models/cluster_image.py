"""
    Cver Api
    Model - Image

"""
from cver.shared.models.cluster_image import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ClusterImage(BaseEntityMeta):

    model_name = "cluster_image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(ClusterImage, self).__init__(conn, cursor)
        self.table_name = "cluster_images"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()


# End File: cver/src/api/modles/cluster_image.py
