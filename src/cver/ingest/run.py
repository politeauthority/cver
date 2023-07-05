""" Cvers Ingest - Run
Collect CVE data

"""
import os

from cver.api.utils import auth

CVER_API_URL = os.environ.get("CVER_API_URL")

HEADERS = {
    "Content-Type": "application/json"
}


class Ingest:

    def run(self):
        print("test creds")
        print("client_id: %s" % auth.generate_client_id())
        print("api_key: %s" % auth.generate_api_key())


if __name__ == "__main__":
    Ingest().run()
