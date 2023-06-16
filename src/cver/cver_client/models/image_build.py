"""
    Cver Client
    Model - ImageBuild

"""
from cver.shared.models.image_build import FIELD_MAP
from cver.cver_client.models.base import Base


class ImageBuild(Base):

    model_name = "image_build"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuild instance."""
        super(ImageBuild, self).__init__()
        self.field_map = FIELD_MAP

    def __repr__(self):
        if self.id:
            return f"<ImageBuild {self.id}>"
        else:
            return "<ImageBuild>"


# End File: cver/src/cver_client/models/image_build.py
