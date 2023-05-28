"""
    Cver - Test - Regression
    Auth
    Verifies that authentication is required on all protected endpoints.

"""

import os
import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")
HEADERS = {
    "client-id": CVER_CLIENT_ID,
    "x-api-key": CVER_API_KEY
}


class TestAuth:

    def test__index_info(self):
        """Test Index Info
        GET /info
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s/info" % (CVER_API_URL),
        }

        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

# End File: cver/tests/regression/api/test_auth.py
