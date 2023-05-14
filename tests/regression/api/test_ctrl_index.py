"""
    Cver - Test - Regression
    CTRL Index
        Checks that all routes on / are working properly.

"""

import os
import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_API_CLIENT_ID = os.environ.get("CVER_API_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_API_KEY")
HEADERS = {
    "client-id": CVER_API_CLIENT_ID,
    "x-api-key": CVER_API_KEY
}

URL_BASE = "/"


class TestApiIndex:

    def test__index_get(self):
        """Tests the Cver index through the Cver Api
        GET /
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "version" in response_json

# End File: cver/tests/regression/api/test_ctrl_index.py
