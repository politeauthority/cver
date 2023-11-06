"""
    Cver - Test - Regression
    CTRL Model - Software
        Checks that all routes on /app are working properly.

"""

import json
import os

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")
URL_BASE = "/app"
URL_MODEL = "app"


class TestApiSoftware(TestApiBase):

    def test__software_get_400(self):
        """Tests a bad request on the Software model through the Cver Api.
        GET /app
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 400

    def test__app_post_200(self):
        """Test Software POST
        POST /app
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": {
                "name": "not-real",
                "url_git": "https://github.com/example/example",
                "url_marketing": "https://example.com/"
            }
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        assert response.status_code == 201

    def test__app_get_200(self):
        """Tests the Software collections through the Cver Api
        GET /app
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": "not-real"
            }
        }
        response = requests.request(**request_args)
        assert response.status_code == 200

    def test__app_delete_200(self):
        """Test Software DELETE
        DELETE /app
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": "not-real"
            }
        }
        response_get = requests.request(**request_args)
        assert response_get.status_code == 200
        response_get_json = response_get.json()
        assert isinstance(response_get_json, dict)
        software_id = response_get_json["object"]["id"]
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, software_id),
        }
        response = requests.request(**request_args)
        assert response.status_code == 202


# End File: cver/tests/regression/api/test_ctrl_software.py
