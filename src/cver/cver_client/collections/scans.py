"""
    Cver Client
    Collections
    Scans

"""
from cver.shared.models.scan import FIELD_MAP
from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


class Scans(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Scans, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "scan"
        self.collection_name = "scans"


# End File: cver/src/cver_client/collections/scans.py
