"""
    Cver Client Unit Test
    Client Model: Image
    Source: cver/src/cver/cver_client/model/image.py

"""

from cver.cver_client.models.image import Image


class TestClientModelImage:

    def test____init__(self):
        """Test the Image Model's initialization.
        :method: Image().__init__
        """
        model = Image()
        assert model
        assert hasattr(model, "api_url")
        assert hasattr(model, "client_id")
        assert hasattr(model, "api_key")
        assert hasattr(model, "token")
        assert hasattr(model, "token_path")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = Image()
        assert str(model) == "<Image>"

        model.id = 1
        assert str(model) == "<Image: 1>"


# End File: cver/tests/cver_client/models/test_client_model_image.py
