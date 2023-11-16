"""
    Cver Engine - Unit Test
    Image Scan
    Source: cver/src/cver/engine/modules/image_scan.py

"""
from cver.engine.modules.image_scan import ImageScan


class TestEngineModulesImageScan:

    def test____init__(self):
        """Test the ImageScan initialization
        :method: ImageScan().__init__
        """
        image_scan = ImageScan()
        assert image_scan
        assert hasattr(image_scan, "image")
        assert hasattr(image_scan, "ib")
        assert hasattr(image_scan, "ibw")
        assert hasattr(image_scan, "process_completed")
        assert hasattr(image_scan, "task")
        assert hasattr(image_scan, "prep_success")
        assert hasattr(image_scan, "image_location")
        assert hasattr(image_scan, "data")


# End File: cver/tests/unit/engine/modules/test_image_scan.py
