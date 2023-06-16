"""
    Cver Client
    Model - Image

"""
from cver.shared.models.image import FIELD_MAP
from cver.cver_client.models.base import Base


class Image(Base):

    model_name = "image"

    def __init__(self, conn=None, cursor=None):
        """Create the Image instance."""
        super(Image, self).__init__()
        self.field_map = FIELD_MAP

    def __repr__(self):
        if self.id:
            return f"<Image {self.id}>"
        else:
            return "<Image>"

# End File: cver/src/cver_client/models/image.py
