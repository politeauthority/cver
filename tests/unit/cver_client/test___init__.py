"""
    Cver Client Unit Test
    Init
    Source: cver/src/cver/cver_client/__init__.py

"""

from cver.cver_client import CverClient


class TestClientInit:

    def test____init__(self):
        """Test the CverClient initialization.
        :method: CverClient().__init__
        """
        client = CverClient()
        assert client
        assert hasattr(client, "client_id")
        assert hasattr(client, "api_key")
        assert hasattr(client, "base_url")
        assert hasattr(client, "token")
        assert hasattr(client, "token_path")
        assert hasattr(client, "token_file")
        assert hasattr(client, "login_attempts")
        assert hasattr(client, "max_login_attempts")

    def test___determine_if_login(self):
        """
        :method: CverClient()._determine_if_login
        """
        client = CverClient()
        assert client._determine_if_login()

# End File: cver/tests/cver_client/test___init__.py
