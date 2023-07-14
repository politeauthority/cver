"""Scanner Model

"""
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.shared.models.scanner import FIELD_MAP


class Scanner(BaseEntityMeta):

    model_name = "scanner"

    def __init__(self, conn=None, cursor=None):
        super(Scanner, self).__init__(conn, cursor)
        self.table_name = 'scanners'
        self.field_map = FIELD_MAP
        self.createable = True
        self.metas = {}
        self.setup()

# End File: cver/src/api/models/scanner.py
