"""
    Cver - Test - Regression
    CTRL Collection - RolePerms
        Checks that all routes on /perms are working properly.

"""

import os
import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")

URL_BASE = "/perms"
URL_MODEL = "perm"


class TestApiPerms(TestApiBase):

    def test__role_perms_get(self):
        """Tests the RolePerms collections through the Cver Api
        GET /perms
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

        assert "object_type" in response_json["info"]
        assert isinstance(response_json["info"]["object_type"], str)
        assert response_json["info"]["object_type"] == URL_MODEL

        assert "objects" in response_json
        assert isinstance(response_json["objects"], list)


# End File: cver/tests/regression/api/test_ctrl_perms.py
