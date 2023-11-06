"""
    Cver Client
    Model
    Task

"""
from cver.shared.models.task import FIELD_MAP
from cver.client.models.base import Base


class Task(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Task, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "task"
        self.setup()

# End File: cver/src/cver_client/models/task.py
