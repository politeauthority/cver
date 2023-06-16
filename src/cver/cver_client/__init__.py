"""
    CverClient

"""
import requests

from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild

CVER_API_URL = "http://localhost:5001"
CVER_CLIENT_ID = "nbmqr36ps3"
CVER_API_KEY = "5nm9-y7ay-umg9-olzl"


class CverClient:

    def __init__(self):
        self.base_url = CVER_API_URL
        self.token = ""
        self.token_path = ""

    def login(self) -> bool:
        """Login to the Cver API"""
        request_args = {
            "headers": {
                "client-id": CVER_CLIENT_ID,
                "x-api-key": CVER_API_KEY,
                "content-type": "application/json"
            },
            "method": "POST",
            "url": "%s/auth" % CVER_API_URL,
        }

        response = requests.request(**request_args)
        if response.status_code != 200:
            print("ERROR: %s logging in" % response.status_code)
            return False
        response_json = response.json()
        self.token = response_json["token"]
        return True

    def get_image(self, image_id):
        params = {
            "id": image_id
        }
        image_resp = self.make_request("image", args=params)
        return image_resp

    def get_image_builds(self):
        image_build_resp = self.make_request("image-builds")
        return image_build_resp

    def make_request(self, url: str, method: str = "GET", args: dict = {}):
        headers = {
            "token": self.token,
            "content-type": "application/json"
        }
        request_args = {
            "headers": headers,
            "method": method,
            "url": f"{self.base_url}/{url}"
        }

        if request_args and method == "GET":
            request_args["params"] = args

        response = requests.request(**request_args)
        if response.status_code > 399 and response.status_code < 500:
            print("WARNING: ISSUE WITH REQUEST")

        response_json = response.json()
        return response_json

    def get_objects(self, objects_response):
        if "objects" not in objects_response:
            print("ERROR")
            return []

        objz = []
        for object_data in objects_response["objects"]:
            if objects_response["info"]["object_type"] == "image-build":
                entity = ImageBuild()
            elif objects_response["info"]["object_type"] == "image":
                entity = Image()
            entity.build(object_data)
            objz.append(entity)
        return objz

    def get_object(self, object_response: dict):
        if "object" not in object_response:
            print("ERROR")
            return {}

        if object_response["object_type"] == "image-build":
            entity = ImageBuild()
        elif object_response["object_type"] == "image":
            entity = Image()
        entity.build(object_response["object"])
        return entity


# End File: cver/src/shared/cver_client/__init__.py
