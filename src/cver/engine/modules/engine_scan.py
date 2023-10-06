"""
    Cver Engine
    Scan

"""
import logging

from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.option import Option
from cver.cver_client.models.scan import Scan
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.engine.utils import scan as scan_util


class EngineScan:
    def __init__(self):
        self.scan_limit = 1
        self.downloaded = 0
        self.scanned = 0
        self.pull_thru_registries = {
            "docker.io": None
        }
        self.api_ibws = {}
        self.api_ibws_current_page = 0
        self.ibws_processed = 0
        self.registry_pull_thru_docker_io = None

    def run(self):
        logging.info("Running Engine Scan")
        self.get_configs()
        self.handle_scans()
        logging.info("Scan process complete!")
        return True

    def handle_scans(self):
        ibws = self.get_image_build_waitings()
        logging.info("Found %s" % len(ibws))
        for ibw in ibws:
            self.ibws_processed += 1
            logging.info("Starting ImageBuild %s waiting. Processing: %s" % (
                self.ibws_processed,
                ibw
            ))
            scanned = self.run_scan(ibw)
            if not scanned:
                logging.warning("Did not complete scan for: %s" % ibw)
                continue
            self.scanned += 1
            if self.scanned >= self.scan_limit:
                logging.info("Completed %s of %s downloads" % (
                    self.scanned,
                    self.scan_limit))
                break
        if self.scanned < self.scan_limit:
            self.handle_downloads()
        return True

    def get_configs(self):
        """Get the registry URL and the pull through locations for registries."""
        reg_url = Option()
        reg_url.get_by_name("registry_url")
        self.registry_url = reg_url.value

        reg_pull_thru_docker = Option()
        reg_pull_thru_docker.get_by_name("registry_pull_thru_docker_io")
        self.pull_thru_registries["docker.io"] = reg_pull_thru_docker.value
        return True

    def run_scan(self, ibw: ImageBuildWaiting) -> bool:
        """Run a single scan."""
        image = Image()
        if not image.get_by_id(ibw.image_id):
            logging.error("Cant find Image by ID: %s" % ibw.image_id)
            return False

        ib = ImageBuild()
        if not ib.get_by_id(ibw.image_build_id):
            logging.error("Cant find ImageBuild by ID: %s" % ibw.image_build_id)
            return False
        scan_result = scan_util.run_trivy(image, ib)
        self.save_scan(ib, scan_result)
        ibw.waiting_for = None
        ibw.waiting = False
        if ibw.save():
            logging.info("Saved: %s" % ibw)
            return True
        else:
            logging.error("Failed to Save: %s" % ibw)
            return False

    def save_scan(self, ib: ImageBuild, scan_result: dict) -> bool:
        """Parse and save a scan to the Cver api."""
        logging.info("Parsing scan results from Trivy")
        vulns = scan_result["Results"][0]["Vulnerabilities"]
        scan = Scan()
        scan.user_id = 1
        scan.image_id = ib.image_id
        scan.image_build_id = ib.id
        scan.scanner_id = 1
        vuln_data = self._parse_scan_vulns(vulns)
        scan.cve_critical_int = vuln_data["cve_critical_int"]
        scan.cve_crticial_nums = vuln_data["cve_high_nums"]
        scan.cve_high_int = vuln_data["cve_high_int"]
        scan.cve_high_nums = vuln_data["cve_high_nums"]
        scan.cve_medium_int = vuln_data["cve_medium_int"]
        scan.cve_medium_nums = vuln_data["cve_medium_nums"]
        scan.cve_low_int = vuln_data["cve_low_int"]
        scan.cve_low_nums = vuln_data["cve_low_nums"]
        scan.cve_unknown_int = vuln_data["cve_unknown_int"]
        scan.cve_unknown_nums = vuln_data["cve_unknown_nums"]
        if scan.save():
            logging.info("Saved Scan results successfully")
            return True
        else:
            logging.warning("Failed to save scan for %s" % ib)
            return False

    def get_image_build_waitings(self):
        self.api_ibws_current_page += 1
        ibw_collect = ImageBuildWaitings()
        the_args = {
            "waiting_for": "scan",
            "page": self.api_ibws_current_page
        }
        ibws = ibw_collect.get(the_args)
        self.api_ibws = ibw_collect.response_last["info"]
        if self.api_ibws_current_page == 1:
            logging.info("Found %s Image Builds waiting for scan" % (
                self.api_ibws["total_objects"]))
        else:
            logging.info("Got page %s of %s of ImageBuilds waiting for scan" % (
                self.api_ibws_current_page,
                self.api_ibws["last_page"]))
        return ibws

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


# End File: cver/src/cver/engine/modules/engine_scan.py
