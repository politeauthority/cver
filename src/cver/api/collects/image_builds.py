"""
    Cver Api - Collection
    ImagesBuilds

"""
from cver.api.collects.base import Base
from cver.api.models.image_build import ImageBuild


class ImageBuilds(Base):
    """Collection class for gathering groups of device macs."""

    collection_name = "image-builds"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(ImageBuilds, self).__init__(conn, cursor)
        self.table_name = ImageBuild().table_name
        self.collect_model = ImageBuild
        self.per_page = 20

# End File: cver/src/api/collects/image_builds.py
