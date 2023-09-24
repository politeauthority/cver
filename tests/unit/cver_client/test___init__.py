"""
    Cver Client Unit Test
    Init
    Source: cver/src/cver/cver_client/__init__.py

"""
import os

import pytest

from cver.cver_client import CverClient


@pytest.fixture(scope="module")
def cver_client_id_empty() -> pytest.fixture():
    os.environ["CVER_CLIENT_ID"] = ""
    return os.environ["CVER_CLIENT_ID"]


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
        client = CverClient(
            client_id="test_client_id",
            api_key="test_api_key",
            api_url="https://google.com")
        assert "test_client_id" == client.client_id
        assert "test_api_key" == client.api_key
        assert "https://google.com" == client.base_url

    @pytest.mark.usefixtures("cver_client_id_empty")
    def test___determine_if_login(self):
        """
        :method: CverClient()._determine_if_login
        """
        client = CverClient()
        assert not client._determine_if_login()

        # assert not client._determine_if_login()

# End File: cver/tests/cver_client/test___init__.py
