"""
    Cver - Test - Regression
    CTRL Index
        Checks that all routes on / are working properly.

"""

import os
import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")
URL_BASE = "/"


class TestApiIndex:

    def login(self) -> bool:
        """Tests the Cver index through the Cver Api
        GET /
        """
        request_args = {
            "headers": {
                "client-id": CVER_CLIENT_ID,
                "x-api-key": CVER_API_KEY,
                "content-type": "application/json"
            },
            "method": "POST",
            "url": "%s/auth" % CVER_API_URL,
        }

        response = requests.request(**request_args)
        if response.status_code != 200:
            print("ERROR: %s logging in" % response.status_code)
            return False
        response_json = response.json()
        self.token = response_json["token"]
        return True

    def test__index_get(self):
        """Tests the Cver index through the Cver Api
        GET /
        """
        request_args = {
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "version" in response_json

    def test__info_get(self):
        """Tests the Cver info through the Cver Api. This test requires a valid JWT.
        GET /info
        """
        assert self.login()
        request_args = {
            "headers": {
                "token": self.token,
                "content-type": "application/json"
            },
            "method": "GET",
            "url": "%s%s/info" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "version" in response_json
        assert "build" in response_json
        assert "build_short" in response_json
        assert "info" in response_json
        assert "model_totals" in response_json
        assert "migration" in response_json

    def test__healthz_get(self):
        """Tests the Cver Api healthz endpoint that Kubernetes uses.
        GET /healthz
        """
        assert self.login()
        request_args = {
            "headers": {
                "content-type": "application/json"
            },
            "method": "GET",
            "url": "%s%s/healthz" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "status" in response_json
        assert "message" in response_json


# End File: cver/tests/regression/api/test_ctrl_index.py
