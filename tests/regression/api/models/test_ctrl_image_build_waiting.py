"""
    Cver - Test - Regression
    CTRL Model - ImageBuildWaiting
    Checks that all routes on /image-build-waiting are working properly.

"""
import os
import json
import random

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "/image-build-waiting"
URL_MODEL = "image-build-waiting"

TEST_MODEL = {
    "image_id": random.randint(1000, 10000),
    "image_build_id": random.randint(1000, 10000),
    "tag": "latest",
    "waiting": True,
    "waiting_for": "download"
}


class TestApiModelImageBuildWaiting(TestApiBase):

    def test__image_build_waiting_get_404(self):
        """ Test that we get a 404 on an image that doesnt exist.
        GET /image-build-waiting
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

    def test__image_build_waiting_post_200(self):
        """ Test that we can create a new Image model.
        POST /image-build-waiting
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

    # def test__image_build_get_200(self):
    #     """Tests fetching a single ImageBuildWaiting through the Cver Api from its name.
    #     GET /image-build-waiting
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

    # def test__image_build_waiting_delete_200(self):
    #     """Test ImageBuildWaiting DELETE
    #     DELETE /image-build-waiting
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

    #     assert response_delete.status_code == 201


# End File: cver/tests/regression/api/test_ctrl_image.py