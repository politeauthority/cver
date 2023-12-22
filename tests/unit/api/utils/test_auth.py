"""
    Cver Test
    Unit
    Test Auth
    Source: src/cver/api/utils/auth.py

"""
from cver.api.utils import auth


class TestApiUtilAuth:

    def test__generate_client_id(self):
        """Test's that we create a client-id that looks like we expect it to.
        :method: auth.generate_client_id()
        """
        client_id = auth.generate_client_id()
        assert len(client_id) == 10

    def test__generate_api_key(self):
        """Test's that we create an api-key that looks like we expect it to.
        :method: auth.generate_api_key()
        """
        api_key = auth.generate_api_key()
        assert len(api_key) == 19
        assert api_key[4] == "-"
        assert api_key[9] == "-"
        assert api_key[14] == "-"

# End File: cver/tests/api/utils/test_auth.py
