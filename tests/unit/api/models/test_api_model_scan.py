"""
    Cver Test Unit
    Api Model: Scan
    Source: src/cver/api/model/scan.py

"""
from datetime import datetime

from cver.api.models.scan import Scan

from cver_test_tools.fixtures import db


class TestApiModelScan:

    def test____init__(self):
        """Test the Scanner Model's initialization.
        :method: Scan().__init__
        """
        model = Scan()
        assert hasattr(model, "user_id")
        assert hasattr(model, "image_id")
        assert hasattr(model, "image_build_id")
        assert hasattr(model, "scanner_id")
        assert hasattr(model, "cve_critical_int")
        assert hasattr(model, "cve_critical_nums")
        assert hasattr(model, "cve_high_int")
        assert hasattr(model, "cve_high_nums")
        assert hasattr(model, "cve_medium_int")
        assert hasattr(model, "cve_medium_nums")
        assert hasattr(model, "cve_low_int")
        assert hasattr(model, "cve_low_nums")
        assert hasattr(model, "cve_unknown_int")
        assert hasattr(model, "cve_unknown_nums")
        assert hasattr(model, "pending_parse")

    def test____repr__(self):
        """Test the model's representation.
        :method: Scan().__repr__
        """
        model = Scan()
        assert str(model) == "<Scan>"

    def test__save(self):
        """Test the model's representation.
        :method: Scan().__repr__
        """
        model = Scan(db.Conn(), db.Cursor())
        model.id = 1
        model.created_ts = datetime.now()
        model.updated_ts = datetime.now()
        model.user_id = 1
        model.image_id = 1
        model.image_build_id = 1
        model.scanner_id = 1
        model.cve_critical_nums = ["CVE-1000", "CVE-1001", "CVE-1002"]
        model.cve_high_nums = ["CVE-1000", "CVE-1001", "CVE-1002"]
        model.cve_medium_nums = ["CVE-1000", "CVE-1001", "CVE-1002"]
        model.cve_low_nums = ["CVE-1000", "CVE-1001", "CVE-1002"]
        model.cve_unknown_nums = ["CVE-1000", "CVE-1001", "CVE-1002"]
        model.pending_parse = True
        assert model.save()
        assert 3 == model.cve_critical_int

# End File: cver/tests/api/models/test_scanner.py
