"""
    Cver - Test - Regression
    CTRL Model - Image
    Checks that all routes on /images are working properly.

"""
import json
import random
import os

import requests

from cver.shared.utils import misc

from .test_api_base import TestApiBase

CVER_API_URL = misc.add_trailing_slash(os.environ.get("CVER_API_URL"))
CVER_CLIENT_ID = os.environ.get("CVER_TEST_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_TEST_API_KEY")
URL_BASE = "/cluster"
URL_MODEL = "cluster"

TEST_MODEL = {
    "name": "My Test Cluster",
    "org_id": random.randint(1000, 2000)
}


class TestApiModelCluster(TestApiBase):

    def test__cluster_get_404(self):
        """ Test that we get a 404 on a model that doesnt exist.
        GET /cluster
        """
        assert self.login()
        random_number = random.randint(5000, 10000)
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": f"{CVER_API_URL}{URL_BASE}/{random_number}",
        }

        response = requests.request(**request_args)
        assert response.status_code == 404

    def test__cluster_post_200(self):
        """ Test that we can create a new model.
        POST /cluster
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": f"{CVER_API_URL}{URL_BASE}",
            "data": TEST_MODEL
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        assert response.status_code == 201

    def test__cluster_get_200(self):
        """Tests fetching a single model through the Cver Api from its name.
        GET /cluster
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

    def test__cluster_delete_200(self):
        """Test cluster DELETE
        DELETE /cluster
        """
        assert self.login()
        # Get the model
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

        # Delete the entity by ID
        entity_id = response_get_json["object"]["id"]
        request_args = {
            "headers": self.get_headers(),
            "method": "DELETE",
            "url": "%s%s/%s" % (CVER_API_URL, URL_BASE, entity_id),
        }
        response_delete = requests.request(**request_args)

        assert 202 == response_delete.status_code


# End File: cver/tests/regression/api/test_ctrl_cluster.py
