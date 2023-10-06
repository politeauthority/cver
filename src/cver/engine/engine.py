"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system.

"""
import argparse
import logging
import logging.config
import subprocess

from cver.shared.utils.log_config import log_config
from cver.shared.utils import misc
from cver.shared.utils import date_utils
from cver.shared.utils import docker
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
# from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.scan import Scan
from cver.cver_client.models.option import Option
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.engine.utils import scan as scan_util
from cver.engine.modules.download import Download

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Engine:
    def __init__(self):
        self.registry_url = None
        self.registry_user = None
        self.registry_password = None
        self.download_limit = 1
        self.downloaded = 0
        self.scan_limit = 1
        self.scanned = 0

    def run(self):
        if not self.preflight():
            logging.critical("Pre flight checks failed.")
            exit(1)
        self.run_downloads()
        # self.run_scans()

    def preflight(self):
        """Check that have a registry to push/pull to/from."""
        reg_url = Option()
        reg_url.get_by_name("registry_url")
        self.registry_url = reg_url.value
        if not self.registry_url:
            logging.error("No registry url found on Cver")
            return False

        reg_user = Option()
        reg_user.get_by_name("registry_user")
        self.registry_user = reg_user.value
        if not self.registry_user:
            logging.error("No registry user found on Cver")
            return False

        reg_pass = Option()
        reg_pass.get_by_name("registry_password")
        self.registry_password = reg_pass.value
        if not self.registry_password:
            logging.error("No registry password found on Cver")
            return False

        reg_pull_thru_docker = Option()
        reg_pull_thru_docker.get_by_name("registry_pull_thru_docker_io")
        self.registry_pull_thru_docker_io = reg_pull_thru_docker.value
        if not self.registry_pull_thru_docker_io:
            logging.error("No registry pull through found on Cver")
            return False

        docker.registry_login(self.registry_url, self.registry_user, self.registry_password)
        return True

    def run_downloads(self):
        """Engine Download runner. Here we'll download images waiting to be pulled down."""
        Download().run()

    def run_scans(self):
        logging.info("Running Engine Scan")
        ibws = self.get_image_build_waitings("scan")
        logging.info(ibws)
        for ibw in ibws:
            self.run_scan(ibw)

    def run_download(self, ibw: ImageBuildWaiting) -> bool:
        """Run a s single download."""
        self.download_image(ibw)

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

    def get_image_build_waitings(self, waiting_for: str):
        """Get the ImageBuildsWaiting for some sort of processing."""
        args = {
            "waiting_for": waiting_for
        }
        ibws = ImageBuildWaitings().get(args)
        # import ipdb; ipdb.set_trace()
        return ibws

    def download_image(self, ibw: ImageBuildWaiting) -> bool:
        """Download the docker image.
        @note: For now we'll assume we always have a pull through cache like Harbor available.
        """
        image = Image()
        if not image.get_by_id(ibw.image_id):
            logging.error("Cannot find Image by ID: %s" % ibw.image_id)
            return False
        pull_through = False
        if image.registry == "docker.io":
            pull_through = True
            image_loc = "%s/%s/%s:%s" % (
                self.registry_url,
                self.registry_pull_thru_docker_io,
                image.name,
                ibw.tag)
        else:
            image_loc = "%s/%s" % (image.registry, image.name)

        pull_cmd = ["docker", "pull", image_loc]

        image_pull = subprocess.check_output(pull_cmd)

        sha = self._get_sha_from_docker_pull(image_pull.decode("utf-8"))
        ib = ImageBuild()
        ib.sha = sha
        ib.image_id = image.id
        ib.registry = image.registry
        if pull_through:
            replace_str = "%s:%s" % (image.name, ibw.tag)
            ib.registry_imported = misc.strip_trailing_slash(image_loc.replace(replace_str, ""))
        ib.tags = [ibw.tag]
        ib.sync_enabled = True
        ib.sync_flag = False
        ib.sync_last_ts = date_utils.json_date_now()
        ib.scan_flag = True
        ib.scan_enabled = True
        ib.pending_operation = "scan"
        if ib.save():
            logging.info("Save: %s" % ib)
        else:
            logging.error("Could not save: %s" % ib)

        ibw.waiting_for = "scan"
        ibw.image_build_id = ib.id
        if ibw.save():
            logging.info("Save: %s" % ibw)
        else:
            logging.error("Could not save: %s" % ibw)
        return True

    def _get_sha_from_docker_pull(self, image_pull: str) -> str:
        """Get the sha from a Docker image pull command."""
        if "sha256" not in image_pull:
            logging.error("Cannot get sha from docker pull command.")
            return False

        tmp = image_pull[image_pull.find("sha256") + 7:]
        tmp = tmp[:tmp.find("\n")]
        return tmp

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


def parse_args(args):
    """Parse CLI args"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
    print(args)
    return parser


if __name__ == "__main__":
    Engine().run()


# End File: cver/src/cver/engine/engine.py
