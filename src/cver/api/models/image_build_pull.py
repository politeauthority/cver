"""
    Cver Api
    Model
    Image Build Pull

"""
from cver.shared.models.image_build_pull import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ImageBuildPull(BaseEntityMeta):

    model_name = "image_build_pull"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuildPull instance."""
        super(ImageBuildPull, self).__init__(conn, cursor)
        self.table_name = "image_build_pulls"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

# End File: cver/src/api/models/image_build_pull.py
