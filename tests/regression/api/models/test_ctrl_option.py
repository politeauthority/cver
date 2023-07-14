"""
    Cver - Test - Regression
    CTRL Model - Role
    Checks that all routes on /role are working properly.

    @ToDo: Checks on Option ACL

"""
import json
import os
import random

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "/option"
URL_MODEL = "option"

TEST_MODEL = {
    "name": "test_option_str",
}


class TestApiModelOption(TestApiBase):

    def test__option_get_404(self):
        """ Test that we get a 404 on an entity that doesnt exist.
        GET /option
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

    def test__option_post_400(self):
        """ Test that we cannot create a brand new entity.
        POST /option
        """
        assert self.login()
        option_data = {
            "name": "option_create",
            "type": "bool",
            "value": True
        }
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": option_data
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        response_json = response.json()
        assert response_json["message"] == "Not allowed to create entity option"
        assert response_json["status"] == "error"
        assert response.status_code == 400

    def test__option_get_200(self):
        """Tests fetching a single Option through the Cver Api from its name.
        GET /option
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": TEST_MODEL["name"]
            }
        }
        response = requests.request(**request_args)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json
        assert response_json["object"]["name"] == TEST_MODEL["name"]

    def test__option_post_201(self):
        """ Test that we can modify an Option
        POST /option
        """
        assert self.login()
        # Get the entity we're going to modify
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": TEST_MODEL["name"]
            }
        }
        response = requests.request(**request_args)
        response_json = response.json()
        entity_id = response_json["object"]["id"]

        # Edit the Entity
        new_value = "new_value_%s" % random.randint(0, 10000)
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, entity_id),
            "data": {
                "value": new_value
            }
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        response_json = response.json()
        assert response_json["status"] == "success"
        assert response.status_code == 201
        assert response_json["object"]["value"] == new_value

        # Pull the Entity back and see if it's modified.
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": TEST_MODEL["name"]
            }
        }
        response = requests.request(**request_args)
        response_json = response.json()
        assert response_json["object"]["value"] == new_value

    def test__option_delete_405(self):
        """Test Option DELETE
        DELETE /option
        """
        assert self.login()
        # Get the image
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, 1),
        }
        response = requests.request(**request_args)
        assert response.status_code == 405


# End File: cver/tests/regression/api/models/test_ctrl_option.py
