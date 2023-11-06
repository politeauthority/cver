"""
    Cver Client
    Model - Image

"""
from cver.shared.models.image import FIELD_MAP
from cver.client.models.base import Base


class Image(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Image, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image"
        self.setup()

    def __repr__(self):
        """Image model representation."""
        if hasattr(self, "name") and self.name and hasattr(self, "id") and self.id:
            return "<Image: %s %s>" % (self.id, self.name)
        if hasattr(self, "id") and self.id:
            return "<%s: %s>" % (self.__class__.__name__, self.id)
        return "<%s>" % self.__class__.__name__

# End File: cver/src/cver_client/models/image.py
