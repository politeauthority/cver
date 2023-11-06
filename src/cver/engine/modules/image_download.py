"""
    Cver Engine
    Image Download
    Downloads a single Image
"""
import logging
import subprocess

from cver.shared.utils import date_utils
from cver.shared.utils import docker
from cver.client.models.image import Image
from cver.client.models.image_build import ImageBuild
from cver.client.models.task import Task
from cver.engine.utils import glow


class ImageDownload:

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
        self.process_completed = False
        self.registry_pullthru_use = False
        self.registry_pullthru_loc = ""

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
            logging.info("Download prep failed for %s %s" % (self.ibw, self.image))
            return self.data
        logging.info("Running Download: %s - %s - %s - %s" % (
            self.image,
            self.ib,
            self.ibw,
            self.task))
        self.execute_download()
        if self.process_completed:
            return self.data
        self.push_image()
        if not self.process_completed:
            self._handle_success_download()
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
        self.task.name = "engine-download"
        self.task.image_id = self.ibw.image_id
        self.task.image_build_id = self.ibw.image_build_id
        self.task.image_build_waiting_id = self.ibw.id
        self.task.start_ts = date_utils.now()
        self.task.status = True
        self.task.status_reason = "downloaded"
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

        # if self.image.registry in glow.registry_info["pull_thrus"]:
        #     self.registry_pullthru_use = True
        #     self.registry_pullthru_loc = glow.registry_info["pull_thrus"][self.image.registry]

        self.prep_success = True

        return True

    def execute_download(self) -> bool:
        """Gets the download location for the image and executes the download."""
        if self.image.registry == glow.registry_info["local"]["url"]:
            logging.info("Image is from local registry, no need to pull, marking as success.")
            self.data["status_reason"] = "Image exists in local registry"
            self.process_completed = True
            return True

        logging.info("Starting download of: %s" % self.image.name)
        image_loc = self.get_docker_pull_url()
        pull_cmd = ["docker", "pull", image_loc]
        logging.info("Pulling: %s" % image_loc)
        image_pull = self.docker_pull(pull_cmd)
        if not image_pull:
            self._handle_error()
            return False

        logging.info("Successfully downloaded: %s" % self.image)
        if not self.ib:
            logging.info("lets create an ibw")
            self._create_ib_from_pull(image_pull.decode("utf-8"))

        # self.data["status_reason"] = "Succeed downloading"
        # self._handle_success_pull()
        return True

    def push_image(self) -> bool:
        """Push an image to a Cver registry that has been downloaded loacally."""
        logging.info("Starting push of %s - %s" % (self.image, self.ib))
        if self.image.registry == "docker.io":
            full_og_image_str = self.image.name
        else:
            full_og_image_str = "%s/%s" % (self.image.registry, self.image.name)
        logging.info("PUSH IMAGE: %s" % full_og_image_str)
        docker_id = docker.get_docker_id(full_og_image_str)
        logging.info("DOCKER ID: %s" % docker_id)
        if not docker_id:
            self.data["status_reason"] = "Failed to get Docker ID from locally pulled image"
            self._handle_error()
            return False
        image_str = "%s/%s/%s:%s" % (
            glow.registry_info["local"]["url"],
            glow.registry_info["repository_general"],
            self.image.name,
            self.ibw.tag
        )
        if not docker.tag_image(docker_id, image_str):
            logging.error("Failed Tagging")
            self.data["status_reason"] = "Failed tagging after download"
            self._handle_error()
            docker.delete_image(docker_id)
            return False
        if not docker.push_image(image_str):
            self.data["status_reason"] = "Failed push to local registry after download"
            logging.error("Failed pushing")
            self._handle_error()
            docker.delete_image(docker_id)
            return False
        docker.delete_image(docker_id)
        return True

    def get_docker_pull_url(self) -> str:
        """Get the appropriate image url to pull from, based on pull through registries that have
        been preset.
        """
        if self.registry_pullthru_use:
            image_loc = "%s/%s/%s" % (
                glow.registry_info["local"]["url"],
                self.registry_pullthru_loc,
                self.image.name)
        else:
            image_loc = "%s/%s" % (self.image.registry, self.image.name)
            logging.warning("No pull through location set for registry: %s" % self.image.registry)

        if self.ibw.tag:
            image_loc += ":%s" % self.ibw.tag
        if self.ib.sha:
            image_loc += "@sha256:%s" % self.ib.sha
        return image_loc

    def docker_pull(self, cmd: list) -> bool:
        try:
            image_pull = subprocess.check_output(cmd)
            print(image_pull)
            logging.info("Successfully pulled image")
            return True
        except subprocess.CalledProcessError as e:
            msg = "Failed running command: %s\n%s" % (" ".join(cmd), e)
            self.data["status_reason"] = msg
            logging.error(msg)
            return False

    def _handle_error(self) -> bool:
        """Handle an error pulling an image."""
        logging.info("Saving Download Error: %s - %s - %s - %s" % (
            self.image, self.ib, self.ibw, self.task))
        self.ib.sync_last_ts = date_utils.json_date_now()

        self.ibw.status = False
        self.ibw.status_ts = date_utils.json_date_now()
        if not self.ibw.fail_count:
            self.ibw.fail_count = 1
        else:
            self.ibw.fail_count += 1
        self.ibw.status = False
        self.ibw.status_reason = self.data["status_reason"]

        self.task.status = False
        self.task.status_reason = self.data["status_reason"]
        self.task.end_ts = date_utils.now()

        self.data["status"] = False
        self.data["status_reason"] = self.data["status_reason"]

        self.process_completed = True
        return self._handle_entity_saves()

    def _handle_success_download(self) -> bool:
        """Handle a success pulling an image."""
        # Handle class data
        self.data["status"] = True
        self.data["status_reason"]

        # Handle IB
        self.ib.sync_last_ts = date_utils.json_date_now()
        # @TODO this will need to be fixed for images not using the generic
        self.ib.registry_imported = "%s/%s" % (
            glow.registry_info["local"]["url"],
            glow.registry_info["repository_general"],
        )

        # Handle IBW
        self.ibw.status = True
        self.ibw.status_reason = self.data["status_reason"]
        self.ibw.status_ts = date_utils.json_date_now()
        self.ibw.waiting_for = "scan"
        self.ibw.fail_count = 0

        # Handle Task
        self.task.status = True
        self.task.status_reason = self.data["status_reason"]
        self.task.end_ts = date_utils.now()

        self.process_completed = True
        return self._handle_entity_saves()

    def _handle_entity_saves(self):
        """Save all entities related to the Image Download, including the ImageBuild,
        ImageBuildWaiting and Task.
        """
        # Save the items
        # Save the ImageBuild
        return_success = True
        if self.ib.save():
            logging.info("Saved IB: %s" % self.ib)
        else:
            logging.error("Failed saving IB: %s" % self.ib)
            return_success = False

        # Save the ImageBuildWaiting
        if self.ibw.save():
            logging.info("Saved IBW: %s" % self.ibw)
        else:
            logging.error("Failed saving IBW: %s" % self.ibw)
            return_success = False

        # Save the Task
        if self.task.save():
            logging.info("Saved Task: %s" % self.task)
        else:
            logging.error("Failied saving Task: %s" % self.task)
            return_success = False

        if return_success:
            return True
        else:
            return False

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

# End File: cver/src/cver/engine/modules/image_download.py
