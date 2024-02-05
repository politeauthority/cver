"""
    Image Download
    Downloads a single Image

"""
import logging
import subprocess

from cver.shared.utils import date_utils
from cver.shared.utils import docker
from cver.client.models.image import Image
from cver.client.models.image_build_pull import ImageBuildPull
from cver.client.models.task import Task
from cver.engine.utils import glow

logger = logging.getLogger(__name__)


class ImageDownload:

    def __init__(self, **kwargs):
        """Setup vars that will be used through out the download process."""
        self.image = None
        self.ib = None
        self.ibp = None
        # self.ibw = None
        if "ib" in kwargs:
            self.ib = kwargs["ib"]
        self.task = None
        self.registry = None
        self.ib_pull = None
        self.prep_success = False
        self.pull_time_elapsed = None
        self.push_time_elapsed = None
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
        self.registries = glow.registry_info["registries"]

    def run(self) -> dict:
        """Run the download process."""
        if not self.preflight_check():
            return self.data
        self.data["image"] = self.image
        self.data["ib"] = self.ib

        if not self.prep_success:
            logger.info("Download prep failed for %s %s" % (self.ibp, self.image))
            return self.data

        logger.info("Running Download: %s - %s - %s - %s" % (
            self.image,
            self.ib,
            self.ibp,
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
        if not self.ib:
            logger.error("PreFlight: Missing required data to perform download.")
            return False
        if self.ib:
            if not self.prep_from_ib():
                logger.error("PreFlight: Couldnt fetch required Image details from Cver Api.")
                return False
        if not self.create_ib_pull():
            logger.error("Failed to create Image Build Pull")
        if not self.create_task():
            logger.error("Failed to create download Task")
            return False
        return True

    def create_ib_pull(self) -> bool:
        """Create an ImageBuildPull for the download job."""
        self.ibp = ImageBuildPull()
        self.ibp.image_id = self.ib.image_id
        self.ibp.image_build_id = self.ib.id
        self.ibp.registry_id = self.registry.id
        # self.ib_pull.task_id = self.task.id

        if self.ibp.save():
            logger.info("Image Build Pull created: %s" % self.ib_pull)
            return True
        else:
            return False

    def create_task(self) -> bool:
        """Create a Task for the download job."""
        self.task = Task()
        self.task.name = "engine-download"
        self.task.image_id = self.ib.image_id
        self.task.image_build_id = self.ib.id
        self.task.task_job_id = self.ibp.id
        # self.task.start_ts = date_utils.now()
        self.task.status = None
        self.task.status_reason = "progressing"
        if self.task.save():
            logger.info("Task created: %s" % self.task)
            return True
        else:
            return False

    def prep_from_ib(self) -> bool:
        """Prepare a download process from an ImageBuild."""
        self.image = Image()
        if not self.image.get_by_id(self.ib.image_id):
            logger.warning("Cant get Image from ID: %s for %s" % (self.ib.image_id, self.ib))
            return False

        if self.ib.registry_id not in self.registries:
            logger.error("Cannot find IB %s registry" % self.ibp)
            return False
        self.registry = self.registries[self.ib.registry_id]
        logger.info("Using registry: %s" % self.registry)
        self.prep_success = True

        return True

    def execute_download(self) -> bool:
        """Gets the download location for the image and executes the download."""
        # Check if the Image Build's registry is the local registry, so we can skip caching it.
        self.download_start = date_utils.now()
        if self.registry.url == glow.registry_info["local"]["url"]:
            logger.info("Image is from local registry, no need to pull, marking as success.")
            self.data["status_download"] = True
            self.data["status_download_reason"] = "Image exists in local registry"
            self.data["status_push"] = None
            self.data["status_push_reason"] = "Image exists in local registry"
            self.process_completed = True
            self.download_end = date_utils.now()
            self._handle_success_download()
            return True
        else:
            print("UNHANDLED")
            exit()

        logger.info("Starting download of: %s" % self.image.name)
        image_loc = self.get_docker_pull_url()
        pull_cmd = ["docker", "pull", image_loc]
        logger.info("Pulling: %s" % image_loc)
        pull_start_time = date_utils.now()
        image_pull = self.docker_pull(pull_cmd)

        if not image_pull:
            self._handle_error(stage="image pull")
            return False
        pull_end_time = date_utils.now()
        logger.info("Successfully downloaded: %s" % self.image)

        if self.registry.url == "docker.io":
            image_search = self.image.name
        else:
            image_search = "%s/%s" % (self.registry.url, self.image.name)
        self.image_docker_id = docker.get_docker_id(image_search)
        docker_image_size = docker.get_image_size(self.image_docker_id)
        if docker_image_size:
            self.ib.size = docker_image_size

        self.pull_time_elapsed = (pull_end_time - pull_start_time).seconds
        return True

    def push_image(self) -> bool:
        """Push an image to a Cver registry that has been downloaded loacally."""
        logging.info("Starting push of %s - %s" % (self.image, self.ib))
        if self.registry.url == "docker.io":
            full_og_image_str = self.image.name
        else:
            full_og_image_str = "%s/%s" % (self.registry.url, self.image.name)
        logging.info("Atempting to push: %s/%s" % (self.registry.url, self.image.name))
        if not self.image_docker_id:
            self.data["status_reason"] = "Failed to get Docker ID from locally pulled image"
            self._handle_error()
            return False

        image_str = "%s/%s/%s:%s" % (
            glow.registry_info["local"]["url"],
            glow.registry_info["repository_general"],
            self.image.name,
            self.ib.tag
        )
        if not docker.tag_image(self.image_docker_id, image_str):
            logging.error("Failed Tagging")
            self.data["status_reason"] = "Failed tagging after download"
            self._handle_error()
            docker.delete_image(self.image_docker_id)
            return False
        logging.info("PUSH IMAGE: %s -> %s" % (full_og_image_str, image_str))
        logging.info("DOCKER ID: %s" % self.image_docker_id)

        push_start_time = date_utils.now()
        if not docker.push_image(image_str):
            self.data["status_reason"] = "Failed push to local registry after download"
            logging.error("Failed pushing")
            self._handle_error()
            docker.delete_image(self.image_docker_id)
            return False
        push_end_time = date_utils.now()
        self.push_time_elapsed = (push_end_time - push_start_time).seconds
        docker.delete_image(self.image_docker_id)
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
            image_loc = "%s/%s" % (self.registry.url, self.image.name)
            logging.warning("No pull through location set for registry: %s" % self.registry.url)

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

    def _handle_error(self, stage: str = None) -> bool:
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
        self.ibw.waiting_for = "download"
        self.ibw.status = False
        self.ibw.status_reason = self.data["status_reason"]

        self.task.status = False
        self.task.status_reason = self.data["status_reason"]
        self.task.end_ts = date_utils.now()

        # Handle IB Pull
        if stage == "image pull":
            self.ib_pull.status = False

        if self.pull_time_elapsed:
            self.ib_pull.status = True
            self.ib_pull.pull_time_elapsed = self.pull_time_elapsed

        self.ib_pull.save()

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

        # Handle Image Build Pull
        self.ibp.task_id = self.task.id
        self.ibp.status_download = self.data["status_download"]
        self.ibp.status_download_reason = self.data["status_download_reason"]

        self.ibp.status_push = self.data["status_push"]
        self.ibp.status_push_reason = self.data["status_push_reason"]
        if not self.ibp.save():
            logger.critical("Could not save IBP: %s" % self.ibp)
            return False

        # Handle Task
        self.task.status = True
        self.task.status_reason = self.data["status_reason"]
        self.task.end_ts = self.download_end

        # Handle IB Pull
        self.ibp.status = True
        self.ibp.status_reason = "Successful pull"
        self.ibp.pull_time_elapsed = self.pull_time_elapsed
        self.ibp.push_time_elapsed = self.push_time_elapsed
        self.ibp.save()
        logger.info("Saved IB Pull: %s" % self.ibp)

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
        if self.ibp.save():
            logging.info("Saved IBP: %s" % self.ibp)
        else:
            logging.error("Failed saving IBP: %s" % self.ibp)
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
