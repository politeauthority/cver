"""
    Cver Api - Collection
    ImagesBuildWaitings

"""
from cver.api.collects.base import Base
from cver.api.models.image_build_waiting import ImageBuildWaiting


class ImageBuildWaitings(Base):
    """Collection class for gathering groups of ImageBuildWaitings"""

    collection_name = "image-build_waitings"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ImageBuildWaitings, self).__init__(conn, cursor)
        self.table_name = ImageBuildWaiting().table_name
        self.collect_model = ImageBuildWaiting
        self.per_page = 20

# End File: cver/src/api/collects/image_build_waitings.py
