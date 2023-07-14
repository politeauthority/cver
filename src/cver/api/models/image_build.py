"""
    Cver Api
    Model - ImageBuild

"""
from cver.shared.models.image_build import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ImageBuild(BaseEntityMeta):

    model_name = "image_build"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuild instance."""
        super(ImageBuild, self).__init__(conn, cursor)
        self.table_name = "image_builds"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()


# End File: cver/src/shared/modles/image_build.py
