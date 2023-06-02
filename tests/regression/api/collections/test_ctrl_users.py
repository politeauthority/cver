"""
    Cver - Test - Regression
    CTRL Users
        Checks that all routes on /users are working properly.

"""

import os
import requests


CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")

URL_BASE = "/users"
URL_MODEL = "user"


class TestApiUsers:

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

    def get_headers(self):
        return {
            "token": self.token,
            "content-type": "application/json"
        }

    def test__users_get(self):
        """Tests the Users collections through the Cver Api
        GET /users
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


# End File: cver/tests/regression/api/collections/test_ctrl_users.py
