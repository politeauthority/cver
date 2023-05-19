"""
    Cver Api
    Model - Image

"""
from cver.shared.models.image import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class Image(BaseEntityMeta):

    model_name = "image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(Image, self).__init__(conn, cursor)
        self.table_name = "images"
        self.field_map = FIELD_MAP
        self.api_writeable_fields = ["name", "repository", "maintained"]
        self.setup()


# End File: cver/src/shared/modles/image.py
