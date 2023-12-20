"""
    Cver Client
    Model
    ImageBuildPull

"""
from cver.shared.models.image_build_pull import FIELD_MAP
from cver.client.models.base import Base


class ImageBuildPull(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ImageBuildPull, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-pull"
        self.setup()

# End File: cver/src/cver_client/models/image_build_pull.py
