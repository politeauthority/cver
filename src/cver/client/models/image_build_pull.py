"""
    Cver Client
    Model
    ImageBuildPull

"""
from cver.shared.models.image_build_pull import FIELD_MAP
from cver.client.models.base import Base


class ImageBuildPull(Base):

    def __init__(self):
        """Create the instance."""
        super(ImageBuildPull, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-pull"
        self.setup()

    def get_by_image_build_id(self, image_build_id: int) -> bool:
        """Get an ImageBuildPull by an ImageBuild ID.
        @todo: Have this order by latest/ greatest IBP ID and write a test for it
        """
        return self.get_by_field("image_build_id", image_build_id)

# End File: cver/src/cver_client/models/image_build_pull.py
