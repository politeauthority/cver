"""
    Cver - Test - Regression
    CTRL Collection - Scans
    Checks that all routes on /scans are working properly.

"""

import os
import requests

from .test_api_base import TestApiBase


CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "/scans"
URL_MODEL = "scan"


class TestApiCollectionScans(TestApiBase):

    def test__scans_get(self):
        """Tests the Scans collections through the Cver Api
        GET /scans
        """
        assert self.login()

        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }
        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        assert "info" in response_json

        assert "current_page" in response_json["info"]
        assert isinstance(response_json["info"]["current_page"], int)

        assert "last_page" in response_json["info"]
        assert isinstance(response_json["info"]["last_page"], int)

        assert "per_page" in response_json["info"]
        assert isinstance(response_json["info"]["per_page"], int)

        assert "total_objects" in response_json["info"]
        assert isinstance(response_json["info"]["total_objects"], int)

        assert "object_type" in response_json
        assert isinstance(response_json["object_type"], str)
        assert response_json["object_type"] == URL_MODEL

        assert "objects" in response_json
        assert isinstance(response_json["objects"], list)


# End File: cver/tests/regression/api/collections/test_ctrl_scans.py