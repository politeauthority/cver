"""
    Cver Api
    Collects - Images

"""
from cver.api.collects.base import Base
from cver.api.models.image_build_pull import ImageBuildPull


class ImageBuildPulls(Base):

    collection_name = "image_build_pulls"

    def __init__(self, conn=None, cursor=None):
        super(ImageBuildPulls, self).__init__(conn, cursor)
        self.table_name = ImageBuildPull().table_name
        self.collect_model = ImageBuildPull
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cver/src/api/collects/image_build_pulls.py
