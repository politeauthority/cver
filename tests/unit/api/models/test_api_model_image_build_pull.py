"""
    Cver Test
    Unit Api
    Api Model: ImageBuildPull
    Source: cver/src/cver/api/model/image_build_pull.py

"""
from cver.api.models.image_build_pull import ImageBuildPull


class TestImageBuildPull:

    def test____init__(self):
        """Test the ImageModelBuild's initialization.
        :method: ImageBuildWaiting().__init__
        """
        model = ImageBuildPull()
        assert hasattr(model, "id")
        assert hasattr(model, "created_ts")
        assert hasattr(model, "updated_ts")
        assert hasattr(model, "image_id")
        assert hasattr(model, "image_build_id")
        assert hasattr(model, "registry_id")
        assert hasattr(model, "status")
        assert hasattr(model, "pull_time")

    def test____repr__(self):
        """Test the model's representation.
        :method: ImageBuildWaiting().__repr__
        """
        model = ImageBuildPull()
        assert str(model) == "<ImageBuildPull>"


# End File: cver/tests/api/models/test_image_build_pull.py
