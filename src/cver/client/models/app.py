"""
    Cver Client
    Model - App

"""
from cver.shared.models.app import FIELD_MAP
from cver.client.models.base import Base


class App(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(App, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "app"
        self.setup()

# End File: cver/src/cver_client/models/app.py
