"""
    Cver Api
    Model - ImageBuildWaiting

"""
from cver.shared.models.image_build_waiting import FIELD_MAP, FIELD_META
from cver.api.models.base_entity_meta import BaseEntityMeta


class ImageBuildWaiting(BaseEntityMeta):

    model_name = "image-build-waiting"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuildWaiting instance."""
        super(ImageBuildWaiting, self).__init__(conn, cursor)
        self.table_name = "image_build_waitings"
        self.field_map = FIELD_MAP
        self.field_meta = FIELD_META
        self.createable = True
        self.insert_iodku = True
        self.setup()

    def get_by_sha(self, sha: str = None) -> bool:
        """Get an ImageBuild by it's sha."""
        if sha:
            self.sha = sha
        return self.get_by_field("sha", self.sha)


# End File: cver/src/api/models/image_build_waiting.py
