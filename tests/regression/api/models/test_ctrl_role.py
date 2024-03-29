"""
    Cver - Test - Regression
    CTRL Model - Role
    Checks that all routes on /role are working properly.

"""
import json
import os
import random

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_API_KEY = os.environ.get("CVER_API_KEY")
CVER_CLIENT_ID = os.environ.get("CVER_CLIENT_ID")
URL_BASE = "/role"
URL_MODEL = "role"

TEST_MODEL = {
    "name": "Test Role",
    "slug_name": "test-role",
}


class TestApiModelRole(TestApiBase):

    def test__role_get_404(self):
        """ Test that we get a 404 on an role that doesnt exist.
        GET /role
        """
        assert self.login()
        random_number = random.randint(1000, 10000)
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, random_number),
        }

        response = requests.request(**request_args)
        assert response.status_code == 404

    def test__role_post_200(self):
        """ Test that we can create a new Role model.
        POST /role
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": TEST_MODEL
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        assert response.status_code == 201

    def test__role_get_200(self):
        """Tests fetching a single Role through the Cver Api from its name.
        GET /role
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "slug_name": TEST_MODEL["slug_name"]
            }
        }
        response = requests.request(**request_args)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json
        assert response_json["object"]["slug_name"] == TEST_MODEL["slug_name"]

    def test__role_delete_200(self):
        """Test Role DELETE
        DELETE /role
        """
        assert self.login()
        # Get the image
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "slug_name": TEST_MODEL["slug_name"]
            }
        }
        response_get = requests.request(**request_args)
        response_get_json = response_get.json()

        # Delete the Image by ID
        entity_id = response_get_json["object"]["id"]
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, entity_id),
        }
        response_delete = requests.request(**request_args)

        assert response_delete.status_code == 202


# End File: cver/tests/regression/api/models/test_ctrl_role.py
