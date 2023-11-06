"""
    Cver - Test - Regression
    CTRL Model - Image
    Checks that all routes on /images are working properly.

"""
import json
import random
import os

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")
URL_BASE = "/user"
URL_MODEL = "user"

TEST_MODEL = {
    "name": "Test Test Contributor",
    "email": "test.test.contributor@example.com",
    "role_slug": "contributor"
}


class TestApiModelUser(TestApiBase):

    def test__user_get_404(self):
        """ Test that we get a 404 on an image that doesnt exist.
        GET /user
        """
        assert self.login()
        random_number = random.randint(100, 1000)
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, random_number),
        }

        response = requests.request(**request_args)
        assert response.status_code == 404

    def test__user_post_200(self):
        """ Test that we can create a new User model.
        POST /user
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
        }

        # Get the contributor role
        request_args["method"] = "GET"
        request_args["url"] = "%s/role" % CVER_API_URL
        request_args["params"] = {
            "slug_name": TEST_MODEL["role_slug"]
        }

        response_role = requests.request(**request_args)
        assert response_role.status_code == 200
        response_role_json = response_role.json()
        assert isinstance(response_role_json, dict)
        role_id = response_role_json["object"]["id"]
        assert isinstance(role_id, int)

        request_args["method"] = "POST"
        request_args["url"] = "%s/user" % CVER_API_URL
        request_args["data"] = {
            "name": TEST_MODEL["name"],
            "email": TEST_MODEL["email"],
            "role_id": role_id,
        }
        request_args["data"] = json.dumps(request_args["data"])
        request_args.pop("params")
        response = requests.request(**request_args)
        assert response.status_code == 201

    def test__user_get_200(self):
        """Tests fetching a single Image through the Cver Api from its name.
        GET /user
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "email": TEST_MODEL["email"]
            }
        }
        response = requests.request(**request_args)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json
        assert isinstance(response_json["object"]["role_id"], int)
        assert response_json["object"]["name"] == TEST_MODEL["name"]
        assert response_json["object"]["email"] == TEST_MODEL["email"]

    def test__user_delete_200(self):
        """Test User DELETE
        DELETE /user
        """
        assert self.login()
        # Get the user
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": TEST_MODEL["name"]
            }
        }
        response_get = requests.request(**request_args)
        response_get_json = response_get.json()

        # Delete the Entity
        entity_id = response_get_json["object"]["id"]
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, entity_id),
        }
        response_delete = requests.request(**request_args)

        assert response_delete.status_code == 202


# End File: cver/tests/regression/api/test_ctrl_user.py
