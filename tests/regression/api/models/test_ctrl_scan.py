"""
    Cver - Test - Regression
    CTRL Model - Scan
    Checks that all routes on /scan are working properly.

"""
import json
import os
import random

import requests

from .test_api_base import TestApiBase

CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "/scan"
URL_MODEL = "scan"

TEST_MODEL = {
    "name": "Test Rol",
    "slug_name": "test-role",
}


class TestApiModelScan(TestApiBase):

    def test__scan_get_404(self):
        """ Test that we get a 404 on an scan that doesnt exist.
        GET /scan
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

    def test_scan_post_201(self):
        """ Test that we can create a new Role model.
        POST /scan
        """
        assert self.login()
        data = {
            "user_id": 1,
            "image_id": 1,
            "image_build_id": 1,
            "scanner_id": 1,
            "cve_critical_int": 2,
            "cve_critical_nums": ["CVE-1000", "CVE-1001"],
            "cve_high_int": 2,
            "cve_high_nums": ["CVE-1000", "CVE-1001"],
            "cve_medium_int": 2,
            "cve_medium_nums": ["CVE-1000", "CVE-1001"],
            "cve_low_int": 2,
            "cve_low_nums": ["CVE-1000", "CVE-1001"],
            "cve_unknown_int": 0,
            "cve_unknown_nums": [],
            "pending_parse": False
        }
        request_args = {
            "headers": self.get_headers(),
            "method": "POST",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": data
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        rj = response.json()
        assert response.status_code == 201
        assert rj["object"]["user_id"] == data["user_id"]
        assert rj["object"]["image_id"] == data["image_id"]
        assert rj["object"]["image_build_id"] == data["image_build_id"]
        assert rj["object"]["scanner_id"] == data["scanner_id"]
        assert rj["object"]["cve_critical_int"] == data["cve_critical_int"]
        assert rj["object"]["cve_critical_nums"] == data["cve_critical_nums"]
        assert rj["object"]["cve_high_int"] == data["cve_high_int"]
        assert rj["object"]["cve_high_nums"] == data["cve_high_nums"]
        assert rj["object"]["cve_medium_int"] == data["cve_medium_int"]
        assert rj["object"]["cve_medium_nums"] == data["cve_medium_nums"]
        assert rj["object"]["cve_low_int"] == data["cve_low_int"]
        assert rj["object"]["cve_low_nums"] == data["cve_low_nums"]
        assert rj["object"]["cve_unknown_int"] == data["cve_unknown_int"]
        assert rj["object"]["cve_unknown_nums"] == data["cve_unknown_nums"]
        assert rj["object"]["pending_parse"] == data["pending_parse"]

    def test_scan_get_200(self):
        """ Test that we can create a new Role model.
        POST /scan
        """
        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "image_id": 1,
                "image_build_id": 1
            }
        }
        response = requests.request(**request_args)
        assert response.status_code == 200

    def test__scan_delete_200(self):
        """Test Scan DELETE
        DELETE /scan
        """
        assert self.login()
        # Get the scan
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "image_id": 1,
                "image_build_id": 1
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
