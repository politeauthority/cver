"""
    Cver - Test - Regression
    CTRL Softwares
        Checks that all routes on /apps are working properly.

"""

import os
import requests


CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_API_CLIENT_ID = os.environ.get("CVER_API_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_API_KEY")
HEADERS = {
    "client-id": CVER_API_CLIENT_ID,
    "x-api-key": CVER_API_KEY
}

URL_BASE = "/images"
URL_MODEL = "image"


class TestApiImages:

    def test__images_get(self):
        """Tests the Images collections through the Cver Api
        GET /images
        """
        request_args = {
            "headers": HEADERS,
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


# End File: cver/tests/regression/api/collections/test_ctrl_images.py
