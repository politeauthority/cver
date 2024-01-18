"""
    Cver Client
    Model
    Scan

"""
from cver.shared.models.scan import FIELD_MAP
from cver.client.models.base import Base


class Scan(Base):

    def __init__(self, conn=None, cursor=None):
        """Create the instance."""
        super(Scan, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "scan"
        self.setup()

    def get_all_cves_as_list(self) -> list:
        """Get all critical, high, medium, low and unknown ints from a scan as a list."""
        cves = []
        if self.cve_critical_int > 0 and self.cve_critical_nums:
            cves += self.cve_critical_nums
        if self.cve_high_int > 0 and self.cve_high_nums:
            cves += self.cve_high_nums
        if self.cve_medium_int > 0 and self.cve_medium_nums:
            cves += self.cve_medium_nums
        if self.cve_low_int > 0 and self.cve_low_nums:
            cves += self.cve_low_nums
        if self.cve_unknown_int > 0 and self.cve_unknown_nums:
            cves += self.cve_unknown_nums
        return cves

# End File: cver/src/cver_client/models/scan.py
