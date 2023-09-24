"""
    Cver Test Regression
    CverClient
    Source: src/cver/cver_client/__init__.py

"""

import os
import tempfile

from cver.cver_client import CverClient


class TestCverClient:

    def test__login(self):
        """Test that we can login to the Cver Api and that we store the token locally in a temp
        file.
        """
        token_file = os.path.join(tempfile.gettempdir(), "cver-token")
        cver = CverClient()
        cver.client_id = os.environ.get("CVER_TEST_CLIENT_ID")
        cver.api_key = os.environ.get("CVER_TEST_API_KEY")
        assert cver.login()
        assert os.path.exists(token_file)

    def test__destroy_token(self):
        """Test that we actually remove the token from the system"""
        token_file = os.path.join(tempfile.gettempdir(), "cver-token")
        cver = CverClient()
        assert cver.destroy_token()
        assert not os.path.exists(token_file)
        assert cver.login()
        assert cver.destroy_token()
        assert not os.path.exists(token_file)

# End File: cver/tests/regression/api/test_auth.py
