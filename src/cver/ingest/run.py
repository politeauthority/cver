""" Cvers Ingest - Run
Collect CVE data

"""
import json
import os
import requests

from cver.shared.utils import log
# from cver.shared.models.cve import Cve
# from cver.shared.models.cvss import Cvss

CVER_API_URL = os.environ.get("CVER_API_URL")

HEADERS = {
    "Content-Type": "application/json"
}


class Ingest:

    def run(self):
        print("hello")
        self.write_app()

    def ingest_vendors(self):
        url = "https://cve.circl.lu/api/browse"
        response = requests.get(url)
        if response.status_code not in [200]:
            print("error getting %s" % url)
            return False
        response_json = response.json()
        print(response_json)

        count = 0
        for vendor in response_json["vendor"]:
            new_vendor = Vendor()
            new_vendor.name = vendor
            new_vendor.save()
            count += 1
        print("Wrote %s Vendors" % count)

    def ingest_products(self):
        """Ingest - Products"""
        vendors = Vendors().get_all()
        import ipdb; ipdb.set_trace() 
        url = "https://cve.circl.lu/api/browse/microsoft"

    def key_word_search(self):
        # url = "https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch=Emby&keywordExactMatch"
        return True

    def ingest_cve(self):
        cve_number = "CVE-2014-1402"
        log.info("Ingest: %s" % cve_number)

        cve = Cve().get_by_number(cve_number)
        url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        response = requests.get(url, params={"cveId": cve_number})
        cvss = Cvss()
        import ipdb; ipdb.set_trace()

    def write_app(self):
        url = "%s/app" % CVER_API_URL
        data = {
            "name": "emby",
            "url_git": "https://github.com/MediaBrowser/Emby",
            "url_marketing": "https://emby.media/"
        }
        data = json.dumps(data)
        response = requests.post(url, data=data, headers=HEADERS)
        print(response)


if __name__ == "__main__":
    Ingest().run()
