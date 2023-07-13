"""
    Cver Api
    Model - ScanRaw

"""
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.shared.models.scan_raw import FIELD_MAP


class ScanRaw(BaseEntityMeta):

    model_name = "scan_raw"

    def __init__(self, conn=None, cursor=None):
        super(ScanRaw, self).__init__(conn, cursor)
        self.table_name = "scan_raws"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.setup()

# End File: cver/src/api/models/scan_raw.py
