"""
    Cver Api
    Model
    Task

"""
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.shared.models.task import FIELD_MAP


class Task(BaseEntityMeta):

    model_name = "task"

    def __init__(self, conn=None, cursor=None):
        super(Task, self).__init__(conn, cursor)
        self.table_name = "tasks"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

# End File: cver/src/api/models/task.py
