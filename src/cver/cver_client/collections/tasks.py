"""
    Cver Client
    Collections - Tasks

"""
from cver.shared.models.task import FIELD_MAP
from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


class Tasks(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(Tasks, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "task"
        self.collection_name = "tasks"


# End File: cver/src/cver_client/collections/tasks.py
