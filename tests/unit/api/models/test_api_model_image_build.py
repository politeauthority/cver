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
        assert hasattr(image, "registry_id")
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
            5,                                      # id
            datetime.now(),                         # created_ts
            datetime.now(),                         # updated_ts
            "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8",
                                                    # sha
            "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8",
                                                    # sha_imported
            10,                                     # image_id
            5,                                      # registry_id
            "harbor.squid-ink.us/cver-general",     # registry_imported
            "tag_1,tag_2",                          # tags
            54123,                                  # size
            "Linux",                                # os_family
            "Alpine",                               # os_name
            1,                                      # maintained
            1,                                      # sync_flag
            1,                                      # sync_enabled
            datetime.now(),                         # sync_last
            1,                                      # scan_flag
            1,                                      # scan_enabled
            datetime.now()                          # scan_last
        ]
        model = ImageBuild(db.Conn(), cursor)
        model.sha = "6937967453147ea7b89333fc2f67f18a19b597d5d62b4d3c22918e7a5b1292f8"
        assert model.get_by_sha("a-fake-client-id")
        assert 10 == model.image_id

# End File: cver/tests/api/models/test_image_build.py
