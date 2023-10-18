"""
    Cver - Test - Regression
    CTRL Collection - Scans
    Checks that all routes on /scans are working properly.

"""
import json
import os
import requests

from cver.cver_client.models.scan import Scan

from .test_api_base import TestApiBase


CVER_API_URL = os.environ.get("CVER_API_URL")
URL_BASE = "/scans"
URL_MODEL = "scan"


class TestApiCollectionScans(TestApiBase):

    def test__scans_get(self):
        """Tests the Scans collections through the Cver Api.
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

    def test_scans_get_cver_score(self):
        """
        """
        assert self.create_test_data()

        assert self.login()
        request_args = {
            "headers": self.get_headers(),
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": {
                "fields": {
                    "cve_critical_int": {
                        "value": 10,
                        "op": ">"
                    }
                }
            }
        }
        request_args["data"] = json.dumps(request_args["data"])
        response = requests.request(**request_args)
        assert response.status_code == 200
        response_json = response.json()
        for scan in response_json["objects"]:
            assert 10 <= scan["cve_critical_int"]

    def create_test_data(self):
        scan_1 = Scan()
        scan_1.user_id = 1
        scan_1.image_id = 1
        scan_1.image_build_id = 1
        scan_1.scanner_id = 1
        scan_1.cve_critical_int = 20497
        scan_1.cve_critical_nums = []
        scan_1.cve_high_int = 1
        scan_1.cve_high_nums = []
        scan_1.cve_medium_int = 1
        scan_1.cve_medium_nums = []
        scan_1.cve_low_int = 1
        scan_1.cve_low_nums = []
        scan_1.cve_unknown_int = 1
        scan_1.cve_unknown_nums = []
        scan_1.pending_parse = 1
        scan_1.save()
        return True

# End File: cver/tests/regression/api/collections/test_ctrl_scans.py
