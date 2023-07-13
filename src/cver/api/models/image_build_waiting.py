"""
    Cver Api
    Model - ImageBuildWaiting

"""
from cver.shared.models.image_build import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ImageBuildWaiting(BaseEntityMeta):

    model_name = "image_build_waiting"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuildWaiting instance."""
        super(ImageBuildWaiting, self).__init__(conn, cursor)
        self.table_name = "image_build_waitings"
        self.field_map = FIELD_MAP
        self.setup()


# End File: cver/src/api/models/image_build_waiting.py
