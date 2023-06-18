"""
    Cver Test Unit
    Api Model: ImageBuild
    Source: cver/src/cver/api/model/image_build.py

"""

from cver.api.models.image_build import ImageBuild


class TestBuild:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: ImageBuild().__init__
        """
        image = ImageBuild()
        assert hasattr(image, "id")
        assert hasattr(image, "created_ts")
        assert hasattr(image, "updated_ts")
        assert hasattr(image, "sha")
        assert hasattr(image, "image_id")
        assert hasattr(image, "repository")
        assert hasattr(image, "tags")
        assert hasattr(image, "os_family")
        assert hasattr(image, "os_name")
        assert hasattr(image, "maintained")
        assert hasattr(image, "scan_flag")
        assert hasattr(image, "scan_enabled")
        assert hasattr(image, "scan_last_ts")
        assert hasattr(image, "pending_operation")

    def test____repr__(self):
        """Test the model's representation.
        :method: ImageBuild().__repr__
        """
        model = ImageBuild()
        assert str(model) == "<ImageBuild>"


# End File: cver/tests/api/models/test_image_build.py
