"""
    CverClient
    Python native interface to communicate with the Cver Api

"""
import json
import logging
import os
import tempfile

import requests


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CverClient:

    def __init__(self):
        self.base_url = os.environ.get("CVER_API_URL")
        self.client_id = os.environ.get("CVER_CLIENT_ID")
        self.api_key = os.environ.get("CVER_API_KEY")
        self.token = ""
        self.token_path = ""
        self.response = None
        temp_dir = tempfile.gettempdir()
        self.token_file = os.path.join(temp_dir, "cver-token")
        self.login_attempts = 0

    def login(self, skip_local_token: bool = False) -> bool:
        """Login to the Cver API."""
        if not skip_local_token and self._open_valid_token():
            return True
        request_args = {
            "headers": {
                "client-id": self.client_id,
                "x-api-key": self.api_key,
                "content-type": "application/json"
            },
            "method": "POST",
            "url": f"{self.base_url}/auth",
        }
        response = requests.request(**request_args)
        if response.status_code != 200:
            print("ERROR: %s logging in" % response.status_code)
            self.login_attempts += 1
            return False
        response_json = response.json()
        self.token = response_json["token"]
        self._save_token()
        return True

    def make_request(self, url: str, method: str = "GET", payload: dict = {}):
        """Make a generic request to the Cver Api. If we don't have a token attempt to login."""
        if not self.token:
            self.login()
        headers = {
            "token": self.token,
            "content-type": "application/json"
        }
        request_args = {
            "headers": headers,
            "method": method,
            "url": f"{self.base_url}/{url}"
        }

        if request_args:
            if method == "GET":
                request_args["params"] = payload
            elif method == "POST":
                request_args["data"] = json.dumps(payload)

        response = requests.request(**request_args)

        # If our token has expired, attempt to get a new one, skipping using the current one.
        if response.status_code == 412:
            self.login(skip_local_token=True)

        if response.status_code > 399 and response.status_code < 500:
            logging.error(f"ISSUE WITH REQUEST: {response}")

        response_json = response.json()
        return response_json

    def submit_scan(self, image_id: int, image_build_id: int, raw_scan: dict):
        """Submit a scan to the Cver Api"""
        payload = {
            "image_id": image_id,
            "image_build_id": image_build_id,
            "scanner_id": 1,
            "raw": raw_scan
        }
        response = self.make_request("submit-scan", "POST", payload)
        print(response)

    def destroy_token(self):
        """Delete a local token from temp space."""
        os.remove(self.token_file)
        logging.info("Deleted local Cver token.")
        return True

    def _save_token(self):
        """Save a token to a local tempfile location."""
        logging.info(f"Temp Dir is: {self.token_file}")
        with open(self.token_file, "w") as temp_file:
            temp_file.write(self.token)
        logging.info(f"Wrote: {temp_file}")
        temp_file.close()
        return True

    def _open_valid_token(self):
        """"If we have an existing server token already on the system, lets use that.
        @todo: Reade the token data to see if it has expired already or not.
        """
        if not os.path.exists(self.token_file):
            return False
        logging.info("Using token file")
        with open(self.token_file, "r") as temp_file:
            token_data = temp_file.read()
        self.token = token_data
        return True


# End File: cver/src/shared/cver_client/__init__.py
