"""
    Cver Client Unit Test
    Client Model: User
    Source: cver/src/cver/cver_client/model/user.py

"""

from cver.client.models.scan import Scan


class TestClientModelUser:

    def test____init__(self):
        """Test the User Model's initialization.
        :method: User().__init__
        """
        scan = Scan()
        assert scan
        assert hasattr(scan, "id")
        assert hasattr(scan, "created_ts")
        assert hasattr(scan, "user_id")
        assert hasattr(scan, "image_id")
        assert hasattr(scan, "image_build_id")
        assert hasattr(scan, "scanner_id")
        assert hasattr(scan, "cve_critical_int")
        assert hasattr(scan, "cve_critical_nums")
        assert hasattr(scan, "cve_high_int")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_medium_int")
        assert hasattr(scan, "cve_medium_nums")
        assert hasattr(scan, "cve_low_int")
        assert hasattr(scan, "cve_low_nums")
        assert hasattr(scan, "cve_unknown_int")
        assert hasattr(scan, "cve_unknown_nums")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "pending_parse")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_high_nums")
        assert hasattr(scan, "cve_high_nums")

    def test____repr__(self):
        """Test the model's representation.
        :method: User().__repr__
        """
        model = Scan()
        assert str(model) == "<Scan>"

        model.id = 1
        assert str(model) == "<Scan: 1>"


# End File: cver/tests/cver_client/models/test_client_model_scan.py
