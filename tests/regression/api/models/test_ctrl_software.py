"""
    Cver - Test - Regression
    CTRL Model - Software
        Checks that all routes on /app are working properly.

"""

import os
import json

import requests

CVER_API_URL = os.environ.get("CVER_API_URL")
CVER_API_CLIENT_ID = os.environ.get("CVER_API_CLIENT_ID")
CVER_API_KEY = os.environ.get("CVER_API_KEY")
HEADERS = {
    "content-type": "application/json",
    "client-id": CVER_API_CLIENT_ID,
    "x-api-key": CVER_API_KEY
}

URL_BASE = "/app"
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
        assert response.status_code == 400

    # def test__app_post_200(self):
    #     """Test Software POST
    #     POST /app
    #     """
    #     request_args = {
    #         "headers": HEADERS,
    #         "method": "POST",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "data": {
    #             "name": "not-real",
    #             "url_git": "https://github.com/example/example",
    #             "url_marketing": "https://example.com/"
    #         }
    #     }
    #     request_args["data"] = json.dumps(request_args["data"])
    #     response = requests.request(**request_args)
    #     assert response.status_code == 200

    # def test__app_get_200(self):
    #     """Tests the Software collections through the Cver Api
    #     GET /app
    #     """
    #     request_args = {
    #         "headers": HEADERS,
    #         "method": "GET",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "params": {
    #             "name": "not-real"
    #         }
    #     }
    #     response = requests.request(**request_args)
    #     assert response.status_code == 200

    # def test__app_delete_200(self):
    #     """Test Software DELETE
    #     DELETE /app
    #     """
    #     request_args = {
    #         "headers": HEADERS,
    #         "method": "GET",
    #         "url": "%s%s" % (CVER_API_URL, URL_BASE),
    #         "params": {
    #             "name": "not-real"
    #         }
    #     }
    #     response_get = requests.request(**request_args)

    #     import ipdb; ipdb.set_trace()

    #     request_args = {
    #         "headers": HEADERS,
    #         "method": "DELETE",
    #         "url": "%s%s/" % (CVER_API_URL, URL_BASE),
    #     }
    #     response = requests.request(**request_args)
    #     assert response.status_code == 200



# End File: cver/tests/regression/api/test_ctrl_software.py
