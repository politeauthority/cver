"""
    Cver Api
    Model - Scan

"""
from cver.api.models.base_entity_meta import BaseEntityMeta
from cver.shared.models.scan import FIELD_MAP


class Scan(BaseEntityMeta):

    model_name = "scan"

    def __init__(self, conn=None, cursor=None):
        super(Scan, self).__init__(conn, cursor)
        self.table_name = "scans"
        self.metas = {}
        self.field_map = FIELD_MAP
        self.setup()

    def save(self) -> int:
        """Save a Scan record, totaling up the number of CVEs at each severity automatically prior
        to save.
        """
        self.cve_critical_int = len(self.cve_critical_nums)
        self.cve_high_int = len(self.cve_high_nums)
        self.cve_medium_int = len(self.cve_medium_nums)
        self.cve_low_int = len(self.cve_low_nums)
        return super(Scan, self).save()

# End File: cver/src/api/models/scan.py
