"""
    Cver Api
    Model - ClusterImage

"""
from cver.shared.models.cluster_image import FIELD_MAP, FIELD_META
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.api.utils import sql_tools


class ClusterImage(BaseEntityMeta):

    model_name = "cluster_image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance.
        :unit-test: TestApiModelClusterImage::test____init__
        """
        super(ClusterImage, self).__init__(conn, cursor)
        self.table_name = "cluster_images"
        self.field_map = FIELD_MAP
        self.field_meta = FIELD_META
        self.createable = True
        self.setup()

    def get_by_cluster_and_image_id(self, cluster_id: int, image_id: int):
        """Get an ClusterImage entity by cluster_id and image_id.
        :unit-test: TestApiModelClusterImage::test____init__
        """
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                `cluster_id` = "%s" AND
                `image_id` = "%s";
        """ % (
            self.table_name,
            sql_tools.sql_safe(cluster_id),
            sql_tools.sql_safe(image_id))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/models/cluster_image.py
