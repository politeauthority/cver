"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system.

"""
import logging
import subprocess

from cver.shared.utils import misc
from cver.shared.utils import date_utils
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.option import Option
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting


class Download:
    def __init__(self):
        self.download_limit = 1
        self.downloaded = 0
        self.pull_thru_registries = {
            "docker.io": None
        }

        self.registry_pull_thru_docker_io = None

    def run(self):
        logging.info("Running Engine Download")
        self.get_configs()
        ibws = self._get_image_build_waitings()
        logging.info("Found %s" % len(ibws))
        for ibw in ibws:
            downloaded = self.run_download(ibw)
            if not downloaded:
                logging.warning("Did not complete download for: %s" % ibw)
                continue
            self.downloaded += 1
            if self.downloaded >= self.download_limit:
                logging.info("Completed %s of %s downloads" % (
                    self.downloaded,
                    self.download_limit))
                break
        logging.info("Download process complete!")
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

    def run_download(self, ibw: ImageBuildWaiting):
        logging.info("Starting downloaded process %s of %s" % (
            self.downloaded,
            self.download_limit))
        image = Image()
        if not image.get_by_id(ibw.image_id):
            logging.error("Cannot find Image by ID: %s" % ibw.image_id)
            return False
        logging.info("Working on: %s" % image)

        if image.registry not in self.pull_thru_registries:
            logging.info("Not pulling image %s registry %s is not in pull through list" % (
                image,
                image.registry
            ))
            return False

        image_loc = self._get_docker_pull_url(image, ibw)
        pull_cmd = ["docker", "pull", image_loc]
        logging.info("Pulling: %s" % image_loc)

        image_pull = self.docker_pull(pull_cmd)
        if not image_pull:
            logging.error("Failed to download: %s" % image)
            exit(1)
            return False

        sha = self._get_sha_from_docker_pull(image_pull.decode("utf-8"))
        ib_args = {
            "image_id": image.id,
            "sha": sha
        }
        ib = ImageBuild()
        if ib.get(ib_args):
            logging.warning("Found already existing ImageBuild: %s" % ib)
        ib.image_id = image.id
        ib.sha = sha
        ib.registry = image.registry
        if image.registry in self.pull_thru_registries:
            replace_str = "%s:%s" % (image.name, ibw.tag)
            ib.registry_imported = misc.strip_trailing_slash(image_loc.replace(replace_str, ""))
        ib.tags = [ibw.tag]
        ib.sync_enabled = True
        ib.sync_flag = False
        ib.sync_last_ts = date_utils.json_date_now()
        ib.scan_flag = True
        ib.scan_enabled = True
        ib.pending_operation = "scan"
        ib.save()
        ibw.waiting_for = "scan"
        ibw.save()

    def docker_pull(self, command):
        try:
            image_pull = subprocess.check_output(command)
        except subprocess.CalledProcessError as e:
            logging.error("Failed running command: %s\n%s" % (command, e))
            return False
        logging.info("Successfully pulled image")
        return image_pull

    def _get_image_build_waitings(self):
        ibw_collect = ImageBuildWaitings()
        ibws = ibw_collect.get({"waiting_for": "download"})
        logging.info("Found %s Image Builds waiting for download")
        return ibws

    def _get_docker_pull_url(self, image: Image, ibw: ImageBuildWaiting):
        if image.registry == "docker.io":
            image_loc = "%s/%s/%s:%s" % (
                self.registry_url,
                self.pull_thru_registries["docker.io"],
                image.name,
                ibw.tag)
            return image_loc
        else:
            image_loc = "%s/%s" % (image.registry, image.name)
            logging.warning("No pull through location set for registry: %s" % image.registry)
            return image_loc

    def _get_sha_from_docker_pull(self, image_pull: str) -> str:
        """Get the sha from a Docker image pull command."""
        if "sha256" not in image_pull:
            logging.error("Cannot get sha from docker pull command.")
            return False

        tmp = image_pull[image_pull.find("sha256") + 7:]
        tmp = tmp[:tmp.find("\n")]
        return tmp

# End File: cver/src/cver/engine/modules/download.py
