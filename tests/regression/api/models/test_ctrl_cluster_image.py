"""
    Cver Test - Regression
    CTRL Model - ClusterImage
    Checks that all routes on /cluter-images are working properly.

"""
# import json
import random
import os

import requests

from cver.api.utils import date_utils

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "cluster-image"
URL_MODEL = "cluster-image"

TEST_MODEL = {
    "image_id": random.randint(1000, 2000),
    "cluster_id": 10,
    "first_seen": date_utils.json_date(date_utils.now()),
    "last_seen": date_utils.json_date(date_utils.now())
}


class TestApiModelCluster(TestApiBase):

    def test__get_404(self):
        """ Test that we get a 404 on a model that doesnt exist.
        GET /cluster-image
        """
        assert self.login()
        random_number = random.randint(5000, 10000)
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, random_number),
        }

        response = requests.request(**request_args)
        assert response.status_code == 404

    # def test__post_200(self):
    #     """ Test that we can create a new model.
    #     POST /cluster-image
    #     """
    #     assert self.login()
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "POST",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "data": TEST_MODEL
    #     }
    #     request_args["data"] = json.dumps(request_args["data"])
    #     response = requests.request(**request_args)
    #     response_json = response.json()
    #     TEST_MODEL_ID = response_json["object"]["id"]
    #     assert isinstance(TEST_MODEL_ID, int)
    #     assert response.status_code == 201

    # def test___get_200(self):
    #     """Tests fetching a single model through the Cver Api from its name.
    #     GET /cluster-image
    #     """
    #     assert self.login()
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "GET",
    #         "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, TEST_MODEL_ID),
    #     }
    #     response = requests.request(**request_args)

    #     assert response.status_code == 200
    #     response_json = response.json()
    #     assert response_json

    # def test__delete_200(self):
    #     """Test model DELETE.
    #     DELETE /cluster-image
    #     """
    #     assert self.login()
    #     # Get the model
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

    #     # Delete the entity by ID
    #     entity_id = response_get_json["object"]["id"]
    #     request_args = {
    #         "headers": self.get_headers(),
    #         "method": "DELETE",
    #         "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, entity_id),
    #     }
    #     response_delete = requests.request(**request_args)

    #     assert response_delete.status_code == 202


# End File: cver/tests/regression/api/test_ctrl_cluster_image.py
