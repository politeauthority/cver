"""
    Cver Test - Regression
    CTRL Model - Registry
    Checks that all routes on /registry are working properly.

"""
# import json
import random
import os

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_API_KEY = os.environ.get("CVER_API_KEY")
CVER_CLIENT_ID = os.environ.get("CVER_CLIENT_ID")
URL_BASE = "/registry"
URL_MODEL = "registry"

TEST_MODEL = {
    "name": "not-real",
    "registry": "https://github.com/example/example"
}


class TestApiModelRegistry(TestApiBase):

    def test__registry_get_404(self):
        """ Test that we get a 404 on an registry that doesnt exist.
        GET /registry
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

    # def test__registry_post_200(self):
    #     """ Test that we can create a new Registry model.
    #     POST /registry
    #     """
    #     assert self.login()
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "POST",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "data": {
    #             "name": "not-real",
    #             "registry": "https://github.com/example/example",
    #             "url_marketing": "https://example.com/"
    #         }
    #     }
    #     request_args["data"] = json.dumps(request_args["data"])
    #     response = requests.request(**request_args)
    #     assert response.status_code == 201

    # def test__image_get_200(self):
    #     """Tests fetching a single Image through the Cver Api from its name.
    #     GET /image
    #     """
    #     assert self.login()
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "GET",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "params": {
    #             "name": TEST_MODEL["name"]
    #         }
    #     }
    #     response = requests.request(**request_args)

    #     assert response.status_code == 200
    #     response_json = response.json()
    #     assert response_json

    # def test__image_delete_200(self):
    #     """Test Software DELETE
    #     DELETE /image
    #     """
    #     assert self.login()
    #     # Get the image
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "GET",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "params": {
    #             "name": TEST_MODEL["name"]
    #         }
    #     }
    #     response_get = requests.request(**request_args)
    #     response_get_json = response_get.json()

    #     # Delete the Image by ID
    #     image_id = response_get_json["object"]["id"]
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "DELETE",
    #         "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, image_id),
    #     }
    #     response_delete = requests.request(**request_args)

    #     assert response_delete.status_code == 202


# End File: cver/tests/regression/api/test_ctrl_registry.py
