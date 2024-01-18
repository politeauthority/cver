"""
    Cver Api
    Model
    Cluster Image Build

"""
from cver.shared.models.cluster_image_build import FIELD_MAP, FIELD_META
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.api.utils import sql_tools


class ClusterImageBuild(BaseEntityMeta):

    model_name = "cluster_image_build"

    def __init__(self, conn=None, cursor=None):
        """Create the instance instance.
        :unit-test: TestApiModelClusterImageBuild::test____init__
        """
        super(ClusterImageBuild, self).__init__(conn, cursor)
        self.table_name = "cluster_image_builds"
        self.field_map = FIELD_MAP
        self.field_meta = FIELD_META
        self.createable = True
        self.setup()

    def get_by_cluster_and_image_build_id(self, cluster_id: int, image_build_id: int) -> bool:
        """Get an ClusterImage entity by cluster_id and image_build_id.
        """
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                `cluster_id` = "%s" AND
                `image_build_id` = "%s";
        """ % (
            self.table_name,
            sql_tools.sql_safe(cluster_id),
            sql_tools.sql_safe(image_build_id))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/models/cluster_image_build.py
