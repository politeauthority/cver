"""
    Cver Client
    Model
    Registry

"""
from cver.shared.models.registry import FIELD_MAP
from cver.client.models.base import Base


class Registry(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Registry, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "registry"
        self.setup()

# End File: cver/src/cver_client/models/registry.py
