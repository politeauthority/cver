"""
    Cver Engine
    Image Scan
    Scans a single Image
"""
import logging


from cver.client.models.image import Image
from cver.client.models.image_build import ImageBuild
from cver.client.models.task import Task
from cver.client.models.scan import Scan
from cver.client.models.image_build_pull import ImageBuildPull
from cver.shared.utils import date_utils
from cver.shared.utils import docker
from cver.engine.utils import scan as scan_util
from cver.engine.utils import glow


class ImageScan:

    def __init__(self, **kwargs):
        self.image = None
        self.ib = None
        self.ibw = None
        self.process_completed = False
        if "ibw" in kwargs:
            self.ibw = kwargs["ibw"]
        self.task = None
        self.registry = None
        self.ib_pull = None
        self.scan_time_elapsed = None
        self.prep_success = False
        self.image_location = ""
        self.data = {
            "image": None,
            "ibw": None,
            "ib": None,
            "status": False,
            "status_reason": None,
        }

new line(s) to replace
            return True
        else:
            return False

    def create_ib_pull(self) -> bool:
        """Create an ImageBuildPull for the scan job."""
        self.ib_pull = ImageBuildPull()
        self.ib_pull.image_id = self.ibw.image_id
        self.ib_pull.image_build_id = self.ibw.id
        self.ib_pull.registry_id = self.registry.id
        self.ib_pull.task_id = self.task.id
        self.ib_pull.job = "scan"
        if self.ib_pull.save():
            logging.info("Image Build Pull created: %s" % self.ib_pull)
            return True
        else:
            return False

    def prep_from_ibw(self) -> bool:
        """Prepare a download process from an ImageBuildWaiting.
        @todo: Merge this with image_download's version of this.
        """
        self.image = Image()
        if not self.image.get_by_id(self.ibw.image_id):
            logging.warning("Cant get Image from ID: %s for %s" % (self.ibw.image_id, self.ibw))
            return False
        
        if self.ibw.status == "Failed":
            self._handle_error_scan()
            return False

        if self.ibw.status == "Failed":
            self.task.status = False
            self.task.status_reason = "failed to download"
            self.task.end_ts = date_utils.json_date_now()
            self.task.save()
            logging.warning(
                "Skipping: %s %s, image has already experienced download failures" % (
                    self.ibw, self.image))
            return False

        if self.ibw.image_build_id:
            self.ib = ImageBuild()
            self.ib.get_by_id(self.ibw.image_build_id)
            logging.debug("Loaded: %s" % self.ib)

        self.registry = glow.registry_info["registries"][self.ibw.registry_id]
        logging.info("Using registry: %s" % self.registry)

        self.prep_success = True

        return True

new line(s) to replace
        return True

    def clean_up(self):
        """
        @todo: remove the docker image from the local machine
        @todo: remove the ibw form cver-api
        """
        print("Lets cleanup")

    def save_scan(self, scan_result: dict) -> bool:
        """Parse and save a scan to the Cver api."""
        logging.info("Parsing scan results from Trivy")
        scan = Scan()
        scan.user_id = 1
        scan.image_id = self.ib.image_id
        scan.image_build_id = self.ib.id
        scan.scanner_id = 1
        if "Vulnerabilities" not in scan_result["Results"][0]:
            logging.warning("No vulnerabilities found in: %s" % self.ib)
            scan.save()
            return True

        vulns = scan_result["Results"][0]["Vulnerabilities"]
        vuln_data = self._parse_scan_vulns(vulns)
        scan.cve_critical_int = vuln_data["cve_critical_int"]
        scan.cve_crticial_nums = vuln_data["cve_critical_nums"]
        scan.cve_high_int = vuln_data["cve_high_int"]
        scan.cve_high_nums = vuln_data["cve_high_nums"]
        scan.cve_medium_int = vuln_data["cve_medium_int"]
        scan.cve_medium_nums = vuln_data["cve_medium_nums"]
        scan.cve_low_int = vuln_data["cve_low_int"]
        scan.cve_low_nums = vuln_data["cve_low_nums"]
        scan.cve_unknown_int = vuln_data["cve_unknown_int"]
        scan.cve_unknown_nums = vuln_data["cve_unknown_nums"]
        scan.time_elapsed = self.scan_time_elapsed
        if scan.save():
            logging.info("Saved Scan results successfully")
            return True
        else:
            logging.warning("Failed to save scan for %s" % self.ib)
            return False

    def _handle_error_scan(self) -> bool:
        """Handle an error pulling an image."""
        self.ib.scan_last = date_utils.now()
        self.ibw.status = False
        self.ibw.status_ts = date_utils.json_date_now()
        if not self.ibw.fail_count:
            self.ibw.fail_count = 1
        else:
            self.ibw.fail_count += 1
        self.ibw.status_reason = self.data["status_reason"]

        self.task.status_reason = self.data["status_reason"]
        self.task.end_ts = date_utils.now()
        self.task.save()

        self.data["status"] = False
        self.data["status_reason"] = self.data["status_reason"]

        self.ib.save()

        if self.ibw.save():
            logging.info("Saved ibw failed download status")
            return True
        else:
            logging.error("Could not save ibw failed status")
            return False

    def _handle_success_scan(self) -> bool:
        """Handle a success scanning an image."""
        # Handle class data
        self.data["status"] = True
        self.data["status_reason"] = "Succeed scanning"

        # Handle IBW
        self.ibw.delete()

        # Handle IB
        self.ib.scan_last_ts = date_utils.json_date_now()
        self.ib.save()

        # Handle Task
        self.task.end_ts = date_utils.now()
        self.task.save()
        return True

    def _parse_scan_vulns(self, vulns: list) -> dict:
        """Parses the scan results for vulnerabilities and hydrates a dict to be used for saving
        them.
        """
        data = {
            "cve_critical_int": 0,
            "cve_critical_nums": [],
            "cve_high_int": 0,
            "cve_high_nums": [],
            "cve_medium_int": 0,
            "cve_medium_nums": [],
            "cve_low_int": 0,
            "cve_low_nums": [],
            "cve_unknown_int": 0,
            "cve_unknown_nums": [],
        }
        for vuln in vulns:
            cve_num = vuln["VulnerabilityID"]
            cve_sev = vuln["Severity"]
            if cve_sev == "CRITICAL":
                if cve_num not in data["cve_critical_nums"]:
                    data["cve_critical_int"] += 1
                    data["cve_critical_nums"].append(cve_num)
            elif cve_sev == "HIGH":
                if cve_num not in data["cve_high_nums"]:
                    data["cve_high_int"] += 1
                    data["cve_medium_nums"].append(cve_num)
            elif cve_sev == "MEDIUM":
                if cve_num not in data["cve_medium_nums"]:
                    data["cve_medium_int"] += 1
                    data["cve_medium_nums"].append(cve_num)
            elif cve_sev == "LOW":
                if cve_num not in data["cve_low_nums"]:
                    data["cve_low_int"] += 1
                    data["cve_unknown_nums"].append(cve_num)
            elif cve_sev == "UNKNOWN":
                if cve_num not in data["cve_unknown_nums"]:
                    data["cve_unknown_int"] += 1
                    data["cve_unknown_nums"].append(cve_num)
            else:
                logging.warning("Uknown CVE severity: %s\n%s" % (cve_sev, vuln))
        return data


# End File: cver/src/cver/engine/modules/image_scan.py
