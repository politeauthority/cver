"""
    Cver Test Unit
    Api Model: ImageBuild
    Source: cver/src/cver/api/model/image_build.py

"""
from datetime import datetime

from cver.api.models.image_build import ImageBuild

from cver_test_tools.fixtures import db


class TestImageBuild:

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
        assert hasattr(image, "registry")
        assert hasattr(image, "tags")
        assert hasattr(image, "os_family")
        assert hasattr(image, "os_name")
        assert hasattr(image, "maintained")
        assert hasattr(image, "scan_flag")
        assert hasattr(image, "scan_enabled")
        assert hasattr(image, "scan_last_ts")

    def test____repr__(self):
        """Test the model's representation.
        :method: ImageBuild().__repr__
        """
        model = ImageBuild()
        assert str(model) == "<ImageBuild>"

    def test__get_by_sha(self):
        """
        :method: ImageBuild().get_by_sha()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(),
            "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8",
            "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8",
            10, "docker.io", 1, "harbor.squid-ink.us/cver-general", "tag_1,tag_2", 54123, "Linux",
            "Alpine", 1, 1, 1, datetime.now(), 1, 1, datetime.now()]
        model = ImageBuild(db.Conn(), cursor)
        model.sha = "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8"
        assert model.get_by_sha("a-fake-client-id")
        assert 10 == model.image_id

# End File: cver/tests/api/models/test_image_build.py
