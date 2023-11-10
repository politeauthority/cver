"""
    Cver - Test - Regression
    Auth
    Verifies that authentication is required on all protected endpoints.

"""

import os
import random

import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
HEADERS = {
    "content-type": "application/json"
}


class TestAuth:

    def create_request_args(self, url: str) -> dict:
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, url),
        }
        return request_args

    def test__index_info(self):
        """Test Index Info
        GET /info
        """
        request_args = self.create_request_args("/info")
        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

    def test__user_index_object_get(self):
        """Test User Object Get
        GET /user/1234
        """
        url = "/user/%s" % str(random.randint(0, 100))
        request_args = self.create_request_args(url)
        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

    def test__users_index_get(self):
        """Test Users Index
        GET /users
        """
        request_args = self.create_request_args("/users")
        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

    def test__apikeys_index_get(self):
        """Test ApiKeys Index
        GET /api-keys
        """
        request_args = self.create_request_args("/api-keys")
        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

    def test__apikey_index_get(self):
        """Test ApiKey /Index
        GET /api-key/{rand-int}
        """
        request_args = self.create_request_args("/api-key/%s" % random.randint(0, 1000))
        response = requests.request(**request_args)
        response_json = response.json()
        assert response.status_code == 401
        assert response_json["status"] == "Error"

# End File: cver/tests/regression/api/test_auth.py
