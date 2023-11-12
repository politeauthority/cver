"""
    Cver Client
    Collections - Options

"""
from cver.shared.models.option import FIELD_MAP
from cver.client.collections.client_collections_base import ClientCollectionsBase


class Options(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Options, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "option"
        self.collection_name = "options"


# End File: cver/src/cver_client/collections/options.py
