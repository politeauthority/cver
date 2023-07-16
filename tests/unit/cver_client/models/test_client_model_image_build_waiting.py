"""
    Cver Client Unit Test
    Client Model: ImageBuildWaiting
    Source: cver/src/cver/cver_client/model/image_build_waiting.py

"""

from cver.cver_client.models.image_build_waiting import ImageBuildWaiting


class TestClientModelImageBuildWaiting:

    def test____init__(self):
        """Test the User Model's initialization.
        :method: User().__init__
        """
        user = ImageBuildWaiting()
        assert user
        assert hasattr(user, "base_url")
        assert hasattr(user, "client_id")
        assert hasattr(user, "api_key")
        assert hasattr(user, "token")
        assert hasattr(user, "token_path")

    def test____repr__(self):
        """Test the model's representation.
        :method: User().__repr__
        """
        model = ImageBuildWaiting()
        assert str(model) == "<ImageBuildWaiting>"

        model.id = 1
        assert str(model) == "<ImageBuildWaiting: 1>"


# End File: cver/tests/cver_client/models/test_client_model_image_build_waiting.py
