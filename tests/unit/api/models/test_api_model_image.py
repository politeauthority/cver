"""
    Cver Test Unit
    Api Model: Image
    Source: src/cver/api/model/image.py

"""

from cver.api.models.image import Image


class TestImage:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: Image().__init__
        """
        image = Image()
        assert hasattr(image, "name")
        assert hasattr(image, "repository")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Image()
        assert str(model) == "<Image>"


# End File: cver/tests/api/models/test_image.py
