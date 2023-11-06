"""
    Cver Client Unit Test
    Client Model: ApiKey
    Source: cver/src/cver/cver_client/model/api_key.py

"""

from cver.client.models.api_key import ApiKey


class TestClientModelApiKey:

    def test____init__(self):
        """Test the ApiKey Model's initialization.
        :method: ApiKey().__init__
        """
        model = ApiKey()
        assert model
        assert hasattr(model, "api_url")
        assert hasattr(model, "client_id")
        assert hasattr(model, "api_key")
        assert hasattr(model, "token")
        assert hasattr(model, "token_path")

    def test____repr__(self):
        """Test the model's representation.
        :method: ApiKey().__repr__
        """
        model = ApiKey()
        assert str(model) == "<ApiKey>"

        model.id = 1
        assert str(model) == "<ApiKey: 1>"


# End File: cver/tests/cver_client/models/test_client_model_api_key.py
