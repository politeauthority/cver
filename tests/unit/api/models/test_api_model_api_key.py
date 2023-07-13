"""
    Cver Test Unit
    Api Model: ApiKey
    Source: src/cver/api/model/api_key.py

"""

from cver.api.models.api_key import ApiKey


class TestApiModelApiKey:

    def test____init__(self):
        """Test the model initialization.
        :method: ApiKey().__init__
        """
        entity = ApiKey()
        assert hasattr(entity, "user_id")
        assert hasattr(entity, "client_id")
        assert hasattr(entity, "key")
        assert hasattr(entity, "last_access")
        assert hasattr(entity, "last_ip")
        assert hasattr(entity, "expiration_date")
        assert hasattr(entity, "enabled")

    def test____repr__(self):
        """Test the model's representation.
        :method: Image().__repr__
        """
        model = ApiKey()
        assert str(model) == "<ApiKey>"

        model.id = 1
        assert str(model) == "<ApiKey: 1>"


# End File: cver/tests/api/models/test_api_model_api_key.py
