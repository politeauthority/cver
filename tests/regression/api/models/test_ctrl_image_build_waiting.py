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
CVER_API_KEY = os.environ.get("CVER_API_KEY")
CVER_CLIENT_ID = os.environ.get("CVER_CLIENT_ID")
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
        """ Test that we can create a new ImageBuildWaiting model. We'll make the request twice
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
        assert 201 == response.status_code
        response_json = response.json()
        image_build_waiting_id = response_json["object"]["id"]

        request_args["method"] = "GET"
        request_args["params"] = {}
        request_args["params"]["image_build_id"] = TEST_MODEL["image_build_id"]
        request_args["params"]["image_id"] = TEST_MODEL["image_id"]
        request_args.pop("data")

        # Make another request
        response = requests.request(**request_args)
        assert 200 == response.status_code
        response_json = response.json()
        image_build_waiting_id_2 = response_json["object"]["id"]
        assert image_build_waiting_id == image_build_waiting_id_2

    def test__image_build_waiting_delete_200(self):
        """Test ImageBuildWaiting DELETE
        DELETE /image-build-waiting
        """
        assert self.login()
        # Get the image
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": json.dumps(TEST_MODEL)
        }
        response = requests.request(**request_args)
        assert 202 == response.status_code


# End File: cver/tests/regression/api/test_ctrl_image.py
