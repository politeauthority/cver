"""
    Cver Client
    Model - Image

"""
from cver.shared.models.image import FIELD_MAP
from cver.cver_client.models.base import Base


class Image(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Image, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image"
        self.setup()

# End File: cver/src/cver_client/models/image.py
