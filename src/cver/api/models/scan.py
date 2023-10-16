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
        self.insert_iodku = False
        self.metas = {}
        self.field_map = FIELD_MAP
        self.createable = True
        self.setup()

    def save(self) -> int:
        """Save a Scan record, totaling up the number of CVEs at each severity automatically prior
        to save.
        """
        if not self.cve_critical_int and self.cve_critical_nums:
            self.cve_critical_int = len(self.cve_critical_nums)
        if not self.cve_high_int and self.cve_high_nums:
            self.cve_high_int = len(self.cve_high_nums)
        if not self.cve_medium_int and self.cve_medium_nums:
            self.cve_high_int = len(self.cve_medium_nums)
        if not self.cve_low_int and self.cve_low_nums:
            self.cve_low_int = len(self.cve_low_nums)
        return super(Scan, self).save()

# End File: cver/src/api/models/scan.py
