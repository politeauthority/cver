"""
    Cver Test
    Unit Api
    Api Model: ImageBuildWaiting
    Source: cver/src/cver/api/model/image_build_waiting.py

"""
from datetime import datetime

from cver.api.models.image_build_waiting import ImageBuildWaiting

from cver_test_tools.fixtures import db


class TestImageBuildWaiting:

    def test____init__(self):
        """Test the ImageModelBuild's initialization.
        :method: ImageBuildWaiting().__init__
        """
        image = ImageBuildWaiting()
        assert hasattr(image, "id")
        assert hasattr(image, "created_ts")
        assert hasattr(image, "updated_ts")
        assert hasattr(image, "image_id")
        assert hasattr(image, "image_build_id")
        assert hasattr(image, "sha")
        assert hasattr(image, "tag")
        assert hasattr(image, "waiting")
        assert hasattr(image, "waiting_for")
        assert hasattr(image, "status")
        assert hasattr(image, "status_ts")
        assert hasattr(image, "status_reason")
        assert hasattr(image, "fail_count")

    def test____repr__(self):
        """Test the model's representation.
        :method: ImageBuildWaiting().__repr__
        """
        model = ImageBuildWaiting()
        assert str(model) == "<ImageBuildWaiting>"

    def test__get_by_sha(self):
        """
        :method: ImageBuildWaiting().get_by_sha()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), 10, 11,
            "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8",
            "a-fake-tag", 1, "download", 1, datetime.now(), "Success", None]
        model = ImageBuildWaiting(db.Conn(), cursor)
        model.sha = "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8"
        assert model.get_by_sha("a-fake-client-id")
        assert 10 == model.image_id


# End File: cver/tests/api/models/test_image_build.py
