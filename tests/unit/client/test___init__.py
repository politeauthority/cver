"""
    Client Unit Test
    Client
    Source: cver/src/cver/client/__init__.py

"""
import os

import pytest

from cver.client import Client as Client


@pytest.mark.vcr
def test_login(self):
    """Test the Client login flow.
    :method: Client().login
    """
    os.environ["CVER_CLIENT_ID"] = "test-client-id"
    os.environ["CVER_API_KEY"] = "test-api-key"
    os.environ["CVER_API_URL"] = "http://localhost/"
    client = Client()
    assert client.login()
    assert os.path.exists(client.token_file)

def test___determine_if_login(self):
    """
    :method: Client()._determine_if_login
    """
    client = Client()
    assert client._determine_if_login()

def test___save_token(self):
    """
    :method: Client()._save_token
    """
    client = Client()
    assert not client._save_token()
    client.token = "fake token!"
    assert client._save_token()

# End File: cver/tests/unit/client/test___init__.py
def test_another_new_method(self):
        """
        :method: Client().another_new_method
        """
        client = Client()
        # Add assertions here to test the another_new_method
        # For example:
        # assert client.another_new_method() == expected_result
#             request.module.__name__)
#     else:
#         return os.path.join(
#             cver_test_dir,
#             "cver_test_tools/vhs/cver-client",
#             request.module.__name__
#         )


# @pytest.fixture(scope='module')
# def vcr_config():
#     """Dont store client-ids or api-keys in casset files"""
#     return {
#         "filter_headers": [
#             ('x-api-key', 'dummy'),
#             ('client-id', 'dummy')
#         ],
#         # "allow_playback_repeats": True
#     }


# @pytest.fixture(scope="module")
# def cver_client_id_empty() -> pytest.fixture():
#     os.environ["CVER_CLIENT_ID"] = ""
#     return os.environ["CVER_CLIENT_ID"]


# @pytest.fixture(scope="module")
# def cver_api_key_id_empty() -> pytest.fixture():
#     os.environ["CVER_API_KEY"] = ""
#     return os.environ["CVER_API_KEY"]


class TestClientInit:

    def test____init__(self):
        """Test the Client initialization.
        :method: Client().__init__
        """
        client = Client()
        assert client
        assert hasattr(client, "client_id")
        assert hasattr(client, "api_key")
        assert hasattr(client, "token")
        assert hasattr(client, "token_file")
        assert hasattr(client, "login_attempts")
        assert hasattr(client, "max_login_attempts")
        client = Client(
            client_id="test_client_id",
            api_key="test_api_key",
            api_url="https://google.com")
        assert "test_client_id" == client.client_id
        assert "test_api_key" == client.api_key

        @pytest.mark.vcr
        def test_new_method(self):
            """
            :method: Client().new_method
            """
            client = Client()
            # Add assertions here to test the new_method
            # For example:
            # assert client.new_method() == expected_result
        def test_login(self):
            """Test the Client login flow.
            :method: Client().login
            """
            os.environ["CVER_CLIENT_ID"] = "test-client-id"
            os.environ["CVER_API_KEY"] = "test-api-key"
            os.environ["CVER_API_URL"] = "http://localhost/"
            client = Client()
            assert client.login()
            assert os.path.exists(client.token_file)

def test___determine_if_login(self):
    """
    :method: Client()._determine_if_login
    """
    client = Client()
    assert client._determine_if_login()

def test___save_token(self):
    """
    :method: Client()._save_token
    """
    client = Client()
    assert not client._save_token()
    client.token = "fake token!"
    assert client._save_token()

# End File: cver/tests/unit/client/test___init__.py

def test___determine_if_login(self):
        def test_new_method(self):
            """
            :method: Client().new_method
            """
            client = Client()
            # Add assertions here to test the new_method
            # For example:
            # assert client.new_method() == expected_result
        def test_login(self):
            """Test the Client login flow.
            :method: Client().login
            """
            os.environ["CVER_CLIENT_ID"] = "test-client-id"
            os.environ["CVER_API_KEY"] = "test-api-key"
            os.environ["CVER_API_URL"] = "http://localhost/"
            client = Client()
            assert client.login()
            assert os.path.exists(client.token_file)

        def test___determine_if_login(self):
        """
        :method: Client()._determine_if_login
        """
        client = Client()
        assert client._determine_if_login()

    def test___save_token(self):
        """
        :method: Client()._save_token
        """
        client = Client()
        assert not client._save_token()
        client.token = "fake token!"
        assert client._save_token()

# End File: cver/tests/unit/client/test___init__.py
