"""
    Cver Test Unit
    Api Model: Scan
    Source: src/cver/api/model/scan.py

"""

from cver.api.models.scan import Scan


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
        :method: Scanner().__repr__
        """
        model = Scan()
        assert str(model) == "<Scan>"


# End File: cver/tests/api/models/test_scanner.py
