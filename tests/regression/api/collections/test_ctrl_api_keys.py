"""
    Cver - Test - Regression
    CTRL ApiKeys
        Checks that all routes on /api-keys are working properly.

"""

import os
import requests


CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")

URL_BASE = "/api-keys"
URL_MODEL = "api-key"


class TestApiApiKeys:

    def login(self) -> bool:
        """Gets a JWT from the Cver api."""
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

    def get_headers(self):
        "Format headers for test requests with the current JWT."
        return {
            "token": self.token,
            "content-type": "application/json"
        }

    def test__api_keys_get(self):
        """Tests the ApiKeys collections through the Cver Api
        GET /api-keys
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "info" in response_json

        assert "current_page" in response_json["info"]
        assert isinstance(response_json["info"]["current_page"], int)

        assert "last_page" in response_json["info"]
        assert isinstance(response_json["info"]["last_page"], int)

        assert "per_page" in response_json["info"]
        assert isinstance(response_json["info"]["per_page"], int)

        assert "total_objects" in response_json["info"]
        assert isinstance(response_json["info"]["total_objects"], int)

        assert "object_type" in response_json["info"]
        assert isinstance(response_json["info"]["object_type"], str)
        assert response_json["info"]["object_type"] == URL_MODEL

        assert "objects" in response_json
        assert isinstance(response_json["objects"], list)
        
        assert len(response_json["objects"]) >= 2

        for api_key in response_json["objects"]:
            assert "key" not in api_key
            assert "id" in api_key


# End File: cver/tests/regression/api/collections/test_ctrl_api_keys.py
