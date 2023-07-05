"""
"""
import os

import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")


class TestApiBase:

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


# End File: cver/tests/regression/api/models/test_api_base.py
