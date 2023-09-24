"""
    Cver Client Unit Test
    Init
    Source: cver/src/cver/cver_client/__init__.py

"""
import os

import pytest

from cver.cver_client import CverClient


@pytest.fixture(scope='module')
def vcr_cassette_dir(request):
    """Put all cassets in the cver_test_tools/vhs/{module}/{test}.yaml dir"""
    return os.path.join(
        "../../",
        "cver_test_tools/vhs/cver-client",
        request.module.__name__)


@pytest.fixture(scope='module')
def vcr_config():
    """Dont store client-ids or api-keys in casset files"""
    return {
        "filter_headers": [
            ('x-api-key', 'dummy'),
            ('client-id', 'dummy')
        ],
    }


@pytest.fixture(scope="module")
def cver_client_id_empty() -> pytest.fixture():
    os.environ["CVER_CLIENT_ID"] = ""
    return os.environ["CVER_CLIENT_ID"]


@pytest.fixture(scope="module")
def cver_api_key_id_empty() -> pytest.fixture():
    os.environ["CVER_API_KEY"] = ""
    return os.environ["CVER_API_KEY"]


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

    @pytest.mark.vcr
    def test_login(self):
        """Test the CverClient login flow.
        :method: CverClient().login
        """
        client = CverClient()
        assert client.login()
        assert os.path.exists(client.token_file)

    @pytest.mark.usefixtures("cver_client_id_empty")
    def test___determine_if_login_no_client_id(self):
        """
        :method: CverClient()._determine_if_login
        """
        client = CverClient()
        assert not client._determine_if_login()

    @pytest.mark.usefixtures("cver_api_key_id_empty")
    def test___determine_if_login_no_api_key(self):
        """
        :method: CverClient()._determine_if_login
        """
        client = CverClient()
        assert not client._determine_if_login()

    def test___determine_if_login(self):
        """
        :method: CverClient()._determine_if_login
        """
        client = CverClient()
        os.environ["CVER_CLIENT_ID"] = "test-client-id"
        os.environ["CVER_API_KEY"] = "test-api-key"
        assert not client._determine_if_login()

    def test___save_token(self):
        """
        :method: CverClient()._save_token
        """
        client = CverClient()
        assert not client._save_token()
        client.token = "fake token!"
        assert client._save_token()

# End File: cver/tests/unit/cver_client/test___init__.py
