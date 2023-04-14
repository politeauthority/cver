"""
    Cver - Test - Regression
    CTRL Software
        Checks that all routes on /app are working properly.

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

URL_BASE = "/apps"
URL_MODEL = "app"


class TestApiSoftware:

    def test__app_get_404(self):
        """Tests the Software collections through the Cver Api
        GET /app
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
        }

        response = requests.request(**request_args)
        assert response.status_code == 404

    def test__app_post_200(self):
        """Test Software POST new
        POST /app
        """
        request_args = {
            "headers": HEADERS,
            "method": "POST",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "data": {
                "name": "not-real",
                "url_git": "https://github.com/example/example",
                "url_marketing": "https://example.com/"
            }
        }
        response = requests.request(**request_args)
        assert response.status_code == 200

    def test__app_get_200(self):
        """Tests the Software collections through the Cver Api
        GET /app
        """
        request_args = {
            "headers": HEADERS,
            "method": "GET",
            "url": "%s%s" % (CVER_API_URL, URL_BASE),
            "params": {
                "name": "not-real"
            }
        }

        response = requests.request(**request_args)
        assert response.status_code == 200

    # def test__app_delete_200(self):
    #     """Test Software DELETE
    #     DELETE /app
    #     """
    #     request_args = {
    #         "headers": HEADERS,
    #         "method": "DELETE",
    #         "url": "%s%s/" % (CVER_API_URL, URL_BASE),
    #     }
    #     response = requests.request(**request_args)
    #     assert response.status_code == 200



# End File: cver/tests/regression/api/test_ctrl_software.py
