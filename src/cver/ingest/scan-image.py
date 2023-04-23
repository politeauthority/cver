"""
    Ingest
    Scan Image

"""

import json
import os

import requests

from cver.shared.utils import log


class ScanImage:

    def __init__(self):
        self.api_url = os.environ.get("CVER_API_URL")
        self.headers = {
            "Content-Type": "application/json"
        }

    def run(self):
        payload = {
            "image_id": 1,
            "image_build": {
                "tags": ["latest"],
                "sha": "7fcaa37bec5e7ab01b1aa8c85503e333684127219b6de179dd117273da25a97e",
                "os_family": "debian",
                "name": "11.6",
            },
            "vulnerabilities": [
                {
                    "number": "CVE-2022-3219",
                    "severity": "LOW",
                    "cvss_score_nvd": 5.5
                }
            ]
        }
        response = requests.post(
            "%s/submit-report" % self.api_url,
            headers=self.headers,
            data=json.dumps(payload))
        if response.status_code >= 400:
            log.error("Error submitting report - Server responded: %s" % response.status_code)
        else:
            log.info("Server responed: %s" % response.status_code)


if __name__ == "__main__":
    ScanImage().run()
