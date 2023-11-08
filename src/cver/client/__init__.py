"""
    Cver Client
    Python native interface to communicate with the Cver Api

"""
import json
import logging
import os
import tempfile

import requests

from cver.shared.utils import misc as s_misc
from cver.shared.utils import xlate
from cver.api.version import version as __version__
from cver.client.utils.config import Config
# from cver.shared.utils.log_config import log_config


# logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Client:

    def __init__(self, client_id=None, api_key=None, api_url=None):
        """Initialize the CverClient with the client_id, api_key and/or api_url. If not supplied
        environmental vars will be attempted.
        """
        self.config = Config().get(client_id, api_key, api_url)
        self.api_url = self.config["api_url"]
        self.client_id = self.config["client_id"]
        self.api_key = self.config["api_key"]

        self.api_url = s_misc.strip_trailing_slash(self.api_url)
        self.user_agent = "CverClient/%s" % __version__

        self.headers = {}
        self.api_host = os.environ.get("CVER_API_HOST")
        self.api_url = s_misc.strip_trailing_slash(self.api_url)

        self.token = ""
        self.token_path = ""
        self.response = None
        temp_dir = tempfile.gettempdir()
        self.token_file = os.path.join(temp_dir, "cver-token")
        self.login_attempts = 0
        self.max_login_attempts = 2
        self.response_last = None

    def login(self, skip_local_token: bool = False) -> bool:
        """Login to the Cver API."""
        logging.debug("Logging into Cver Api: %s" % self.api_url)
        if not skip_local_token and self._open_valid_token():
            return True
        if not self._determine_if_login():
            return False
        request_args = {
            "headers": {
                "client-id": self.client_id,
                "x-api-key": self.api_key,
                "content-type": "application/json"
            },
            "method": "POST",
            "url": f"{self.api_url}/auth",
        }
        request_args["headers"].update(self.headers)
        response = requests.request(**request_args)
        if response.status_code == 403:
            logging.error("Received status code %s logging in" % response.status_code)
            self.login_attempts += 1
            self.login(skip_local_token=True)
            return False
        if response.status_code != 200:
            logging.error("Error authenticating to api")
            return False
        response_json = response.json()
        self.token = response_json["token"]
        self._save_token()
        logging.info("Successfully authenticated to Cver")
        return True

    def make_request(self, url: str, method: str = "GET", payload: dict = {}):
        """Make a generic request to the Cver Api. If we don't have a token attempt to login. Return
        the response json back.
        @todo: Break this apart - too complex
        """
        self.login()
        # if not self.token:
        #     self.login()
        headers = {
            "token": self.token,
            "content-type": "application/json",
            "User-Agent": self.user_agent
        }
        if self.api_host:
            headers["Host"] = self.api_host
        request_args = {
            "headers": headers,
            "method": method,
            "url": f"{self.api_url}/{url}"
        }

        request_args["headers"].update(self.headers)

        if request_args:
            if method == "GET":
                apply_query_field = False
                if isinstance(payload, dict) and "query" in payload:
                    apply_query_field = True
                if apply_query_field:
                    request_args["url"] += "?query=" + xlate.url_encode_json(
                        "%s" % payload["query"])
                else:
                    request_args["params"] = payload

            elif method == "POST":
                request_args["data"] = json.dumps(payload)
                if "id" in payload:
                    request_args["url"] += "/%s" % payload["id"]
                    payload.pop("id")
        # debug
        # logging.info("\n\n%s - %s\n%s" % (
        #     request_args["method"],
        #     request_args["url"],
        #     request_args))
        response = requests.request(**request_args)

        # If our token has expired, attempt to get a new one, skipping using the current one.
        if response.status_code in [412, 401]:
            self.destroy_token()
            # @todo we need to retry here

        if response.status_code > 399:
            if response.status_code == 404:
                logging.debug(f"Got 404: {response.url}")
            else:
                self._handle_error(response, request_args)
                return {}

        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            logging.error("Could not get json from response.\n%s" % response.text)
            return False
        return response_json

    def info(self):
        """Get Cver Api Info"""
        response = self.make_request("info")
        self.response_last = response
        return response

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

    def destroy_token(self) -> bool:
        """Delete a local token from temp space."""
        if not os.path.exists(self.token):
            logging.error("Cant delete token that doesnt exist")
            return True
        os.remove(self.token_file)
        logging.info("Deleted local Cver token.")
        return True

    def _determine_if_login(self) -> bool:
        """Determine if we should even attempt to login.
        :unit-test: TestClientInit::test___determine_if_login
        """
        if not self.client_id or not self.api_key:
            logging.critical("No Client ID or ApiKey submitted, both are required.")
            return False
        if self.login_attempts >= self.max_login_attempts:
            logging.critical("Attemped %s logins, not attempting more" % self.login_attempts)
            return False
        return True

    def _save_token(self):
        """Save a token to a local tempfile location."""
        logging.info(f"Temp Dir is: {self.token_file}")
        if not self.token:
            logging.error("No token to save.")
            return False
        with open(self.token_file, "w") as temp_file:
            temp_file.write(self.token)
        logging.info(f"Wrote: {temp_file}")
        temp_file.close()
        return True

    def _open_valid_token(self):
        """"If we have an existing server token already on the system, lets use that.
        @todo: Reade the token data to see if it has expired already or not.
        """
        # logging.debug("Token File: %s" % self.token_file)
        if not os.path.exists(self.token_file):
            return False
        # logging.debug("Using token file")
        with open(self.token_file, "r") as temp_file:
            token_data = temp_file.read()
        self.token = token_data
        return True

    def _handle_error(self, response, request_args) -> bool:
        url = request_args["url"]
        if "token" in request_args:
            request_args.pop("token")
        if "x-api-key" in request_args:
            request_args.pop("x-api-key")
        msg = f"\nISSUE WITH REQUEST: {response.status_code} - {url}\n"
        msg += f"Api was sent: {request_args}\n"
        msg += f"API Repsonsed: {response.text}\n"
        logging.error(msg)
        return False


# End File: cver/src/shared/cver_client/__init__.py
