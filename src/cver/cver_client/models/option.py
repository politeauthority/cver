"""
    Cver Client
    Model - Option

"""
from cver.shared.models.option import FIELD_MAP
from cver.cver_client.models.base import Base


class Option(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Option, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "option"
        self.setup()

# End File: cver/src/cver_client/models/option.py
