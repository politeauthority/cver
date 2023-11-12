"""
    Cver Test Unit
    Api Model: ApiKey
    Source: src/cver/api/model/api_key.py

"""
from datetime import datetime

from cver.api.models.api_key import ApiKey

from cver_test_tools.fixtures import db


class TestApiModelApiKey:

    def test____init__(self):
        """Test the model initialization.
        :method: ApiKey().__init__
        """
        entity = ApiKey()
        entity.setup()
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

    def test__get_by_cluster_and_image_id(self):
        """Test the model's representation.
        :method: ApiKey().get_by_client_id()
        """
        cursor = db.Cursor()
        cursor.result_to_return = [
            5, datetime.now(), datetime.now(), 10, "a-fake-client-id", "a-fake-api-key",
            datetime.now(), "192.168.1.1", None, 1]
        model = ApiKey(db.Conn(), cursor)
        assert model.get_by_client_id("a-fake-client-id")
        assert 5 == model.id

# End File: cver/tests/api/models/test_api_model_api_key.py
