"""
    Cver Engine
    Image Scan
    Scans a single Image
"""
import logging
import subprocess

from cver.shared.utils import date_utils
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.models.task import Task
from cver.engine.utils import glow
from cver.engine.utils import scan as scan_util


class ImageScan:

    def __init__(self, **kwargs):
        self.image = None
        self.ib = None
        self.ibw = None
        if "ibw" in kwargs:
            self.ibw = kwargs["ibw"]
        self.task = None
        self.prep_success = False
        self.data = {
            "image": None,
            "ibw": None,
            "ib": None,
            "status": False,
            "status_reason": None,
        }

    def run(self, ) -> dict:
        """Run the download process."""
        if not self.preflight_check():
            return self.data

        self.create_task()
        if self.ibw:
            self.prep_from_ibw()
        self.data["image"] = self.image
        self.data["ibw"] = self.ibw
        self.data["ib"] = self.ib
        if not self.prep_success:
            logging.info("Scan prep failed for %s %s" % (self.ibw, self.image))
            return self.data
        self.execute_scan()
        return self.data

    def preflight_check(self) -> bool:
        """Checks to make sure we have the information required to start the download process."""
        if not self.ibw and not self.ib:
            logging.error("Missing required data to perform download.")
            return False
        return True

    def create_task(self) -> bool:
        """Create a Task for the download job."""
        self.task = Task()
        self.task.name = "engine-scan"
        self.task.image_id = self.ibw.image_id
        self.task.image_build_id = self.ibw.image_build_id
        self.task.image_build_waiting_id = self.ibw.id
        self.task.start_ts = date_utils.now()
        self.task.status = True
        self.task.status_reason = "scanned"
        if self.task.save():
            logging.info("Task created: %s" % self.task)
            return True
        else:
            return False

    def prep_from_ibw(self) -> bool:
        """Prepare a download process from an ImageBuildWaiting."""
        self.image = Image()
        if not self.image.get_by_id(self.ibw.image_id):
            logging.warning("Cant get Image from ID: %s for %s" % (self.ibw.image_id, self.ibw))
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

        self.prep_success = True

        return True

    def execute_scan(self):
        """Gets the download location for the image and executes the download."""
        logging.info("Starting scan of: %s" % self.image.name)
        scan_result = scan_util.run_trivy(self.image, self.ib)
        import ipdb; ipdb.set_trace()

        if not scan_result:
            logging.error("Scan failed")
            return False
        logging.info("Successfully downloaded: %s" % self.image)
        if not self.ib:
            logging.info("lets create an ibw")
            self._create_ib_from_pull(image_pull.decode("utf-8"))

        self._handle_success_pull()
        return True

    def get_docker_pull_url(self) -> str:
        """Get the appropriate image url to pull from, based on pull through registries that have
        been preset.
        """
        if self.image.registry in glow.registry_info["pull_thrus"]:
            image_loc = "%s/%s/%s:%s" % (
                glow.registry_info["local"]["url"],
                glow.registry_info["pull_thrus"][self.image.registry],
                self.image.name,
                self.ibw.tag)
            return image_loc
        else:
            image_loc = "%s/%s" % (self.image.registry, self.image.name)
            logging.warning("No pull through location set for registry: %s" % self.image.registry)
            return image_loc

    def docker_pull(self, command):
        try:
            image_pull = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            msg = "Failed running command: %s\n%s" % (command, e)
            self.data["status_reason"] = msg
            logging.error(msg)
            return False
        logging.info("Successfully pulled image")
        return image_pull

    def _handle_error_pull(self) -> bool:
        """Handle an error pulling an image."""
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
        if self.ibw.save():
            logging.info("Saved ibw failed download status")
            return True
        else:
            logging.error("Could not save ibw failed status")
            return False

    def _handle_success_pull(self) -> bool:
        """Handle a success pulling an image."""
        # Handle class data
        self.data["status"] = True
        self.data["status_reason"] = "Succeed downloading"
        # Handle IBW
        self.ibw.status = True
        self.ibw.status_ts = date_utils.json_date_now()
        self.ibw.waiting_for = "scan"
        self.ibw.save()
        # Handle IB
        self.ib.sync_last_ts = date_utils.json_date_now()
        self.ib.save()
        # Handle Task
        self.task.end_ts = date_utils.now()
        self.task.save()
        return True

    def _get_sha_from_docker_pull(self, image_pull: str) -> str:
        """Get the sha from a Docker image pull command."""
        if "sha256" not in image_pull:
            logging.error("Cannot get sha from docker pull command.")
            return False

        tmp = image_pull[image_pull.find("sha256") + 7:]
        tmp = tmp[:tmp.find("\n")]
        return tmp

    def _create_ib_from_pull(self, image_pull: str):
        # sha = self._get_sha_from_docker_pull(image_pull.decode("utf-8"))
        logging.critical("NEED TO WRITE THIS CODE!")
        exit(1)
        # ib_args = {
        #     "image_id": image.id,
        #     "sha": sha
        # }

# End File: cver/src/cver/engine/modules/image_scan.py
