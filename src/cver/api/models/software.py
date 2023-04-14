"""Model - Software

"""
from cver.api.models.base import Base
from cver.api.utils import xlate
from cver.shared.models.software import FIELD_MAP


class Software(Base):

    model_name = "software"

    def __init__(self, conn=None, cursor=None):
        """Create the Software instance."""
        super(Software, self).__init__(conn, cursor)
        self.table_name = "softwares"
        self.field_map = FIELD_MAP
        self.api_writeable_fields = ["name", "slug_name", "url_git",  "url_marketing"]
        self.setup()

# End File: cver/src/shared/modles/software.py
