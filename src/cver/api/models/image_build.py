"""
    Cver Api
    Model
    ImageBuild

"""
from cver.shared.models.image_build import FIELD_MAP
from cver.api.models.base_entity_meta import BaseEntityMeta


class ImageBuild(BaseEntityMeta):

    model_name = "image_build"

    def __init__(self, conn=None, cursor=None):
        """Create the ImageBuild instance."""
        super(ImageBuild, self).__init__(conn, cursor)
        self.table_name = "image_builds"
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def get_by_sha(self, sha: str = None) -> bool:
        """Get an ImageBuild by it's sha."""
        if sha:
            self.sha = sha
        return self.get_by_field("sha", self.sha)

# End File: cver/src/api/models/image_build.py
