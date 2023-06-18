"""
    Cver Client Unit Test
    Client Model: User
    Source: cver/src/cver/cver_client/model/user.py

"""

from cver.cver_client.models.user import User


class TestClientModelUser:

    def test____init__(self):
        """Test the User Model's initialization.
        :method: User().__init__
        """
        user = User()
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
        model = User()
        assert str(model) == "<User>"

        model.id = 1
        assert str(model) == "<User: 1>"


# End File: cver/tests/cver_client/models/test_client_model_user.py
