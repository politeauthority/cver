"""
    Cver Api
    Collection
    Tasks

"""
from cver.api.collects.base import Base
from cver.api.models.task import Task


class Tasks(Base):

    collection_name = "tasks"

    def __init__(self, conn=None, cursor=None):
        super(Tasks, self).__init__(conn, cursor)
        self.table_name = Task().table_name
        self.collect_model = Task
        self.field_map = self.collect_model().field_map
        self.per_page = 20

# End File: cve/src/api/collects/task.py
