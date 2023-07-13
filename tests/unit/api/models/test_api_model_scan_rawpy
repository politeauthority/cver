"""
    Cver Test Unit
    Api Model: ScanRaw
    Source: src/cver/api/model/scan_raw.py

"""

from cver.api.models.scan_raw import ScanRaw


class TestApiModelScanRaw:

    def test____init__(self):
        """Test the model's initialization.
        :method: ScanRaw().__init__
        """
        model = ScanRaw()
        assert hasattr(model, "image_id")
        assert hasattr(model, "image_build_id")
        assert hasattr(model, "scanner_id")
        assert hasattr(model, "scan_id")
        assert hasattr(model, "raw")

    def test____repr__(self):
        """Test the model's representation.
        :method: ScanRaw().__repr__
        """
        model = ScanRaw()
        assert str(model) == "<ScanRaw>"


# End File: cver/tests/api/models/test_api_model_scan_raw.py
