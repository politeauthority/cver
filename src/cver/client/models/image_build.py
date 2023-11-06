"""
    Cver Client
    Model - ImageBuild

"""
from cver.shared.models.image_build import FIELD_MAP
from cver.client.models.base import Base


class ImageBuild(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ImageBuild, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build"
        self.setup()


# End File: cver/src/cver_client/models/image_build.py
