"""
    Cver Client
    Model - ImageBuildWaiting

"""
from cver.shared.models.image_build_waiting import FIELD_MAP
from cver.client.models.base import Base


class ImageBuildWaiting(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(ImageBuildWaiting, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-waiting"
        self.setup()

    def get_by_sha(self, sha: str = None):
        """Get an ImageBuildWaiting by its container sha hash."""
        if sha:
            self.sha = sha
        return self.get_by_field("sha", self.sha)

# End File: cver/src/cver_client/models/image_build_waiting.py
