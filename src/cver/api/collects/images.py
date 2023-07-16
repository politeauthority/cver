"""
    Cver Api
    Collects - Images

"""
from cver.api.collects.base import Base
from cver.api.models.image import Image


class Images(Base):

    collection_name = "images"

    def __init__(self, conn=None, cursor=None):
        """Store database conn/connection and model table_name as well as the model obj for the
           collections target model.
        """
        super(Images, self).__init__(conn, cursor)
        self.table_name = Image().table_name
        self.collect_model = Image
        self.per_page = 20

# End File: cver/src/api/collects/images.py
