"""
    Cver Client Unit Test
    Client Model: ImageBuild
    Source: cver/src/cver/cver_client/model/image_build.py

"""

from cver.client.models.image_build import ImageBuild


class TestClientModelImageBuild:

    def test____init__(self):
        """Test the ImageBuild Model's initialization.
        :method: ImageBuild().__init__
        """
        model = ImageBuild()
        assert model
        assert hasattr(model, "api_url")
        assert hasattr(model, "client_id")
        assert hasattr(model, "api_key")
        assert hasattr(model, "token")
        assert hasattr(model, "token_file")

    def test____repr__(self):
        """Test the model's representation.
        :method: ImageBuild().__repr__
        """
        model = ImageBuild()
        assert str(model) == "<ImageBuild>"

        model.id = 1
        assert str(model) == "<ImageBuild: 1>"


# End File: cver/tests/cver_client/models/test_client_model_image_build.py
