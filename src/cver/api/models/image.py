"""
    Cver Api
    Model - Image

"""
from cver.shared.models.image import FIELD_MAP, FIELD_META
from cver.shared.utils import xlate
from cver.api.models.base_entity_meta import BaseEntityMeta


class Image(BaseEntityMeta):

    model_name = "image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(Image, self).__init__(conn, cursor)
        self.table_name = "images"
        self.field_map = FIELD_MAP
        self.field_meta = FIELD_META
        self.createable = True
        self.setup()

    def get_by_repo_and_name(self, registry: str, name: str):
        """Get an Image entity by repo and image name."""
        sql = """
            SELECT *
            FROM `%s`
            WHERE
                `repository` = "%s" AND
                `name` = "%s";
        """ % (
            self.table_name,
            xlate.sql_safe(registry),
            xlate.sql_safe(name))
        self.cursor.execute(sql)
        raw = self.cursor.fetchone()
        if not raw:
            return False
        self.build_from_list(raw)
        return True

# End File: cver/src/api/modles/image.py
