"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system.

"""
import logging
import subprocess

from cver.cver_client.models.image import Image
# from cver.cver_client.models.image_build import ImageBuild
# from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.option import Option
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting


class Engine:
    def __init__(self):
        self.registry_url = None
        self.registry_user = None
        self.registry_password = None
        self.download_limit = 1
        self.downloaded = 0

    def run(self):
        if not self.preflight():
            logging.critical("Pre flight checks failed.")
            exit(1)
        ibws = self.get_image_build_waitings()
        for ibw in ibws:
            self.determine_work(ibw)

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

        self.registry_login()
        return True

    def registry_login(self):
        """Login to the registry Cver has been instructed to use."""
        cmd = [
            "echo", self.registry_password, "|", "docker", "login", self.registry_url, "--username",
            self.registry_user, "--password-stdin"
        ]
        result = subprocess.check_output(cmd)
        print(result)
        if not result:
            return False
        logging.info("Authenticated to registry: %s" % self.registry_url)
        return True

    def get_image_build_waitings(self):
        """Get the ImageBuildsWaiting for some sort of processing."""
        ibws = ImageBuildWaitings().get()
        return ibws

    def determine_work(self, ibw):
        """Determine what work needs to be done for the ImageBuildWaiting. This breaks down to the
        following scenarios.
            - The IBW is missing an image_build_id, and we need to download a build to the registry.

        """
        if not ibw.image_build_id:
            self.download_latest_image(ibw)
        else:
            logging.warning("Not sure what to do with ImageBuildWaiting: %s" % ibw)

    def download_latest_image(self, ibw: ImageBuildWaiting):
        """Download the docker image.
        @note: For now we'll assume we always have a pull through cache like Harbor available.
        """
        image = Image()
        image.get_by_id(ibw.image_id)
        if image.repository == "docker.io":
            image_loc = "%s/%s/%s" % (
                self.registry_url,
                self.registry_pull_thru_docker_io,
                image.name)
        else:
            image_loc = "%s/%s" % (image.repository, image.name)

        pull_cmd = ["docker", "pull", image_loc]
        print(pull_cmd)

        image_pull = subprocess.check_output(pull_cmd)
        print(image_pull)


if __name__ == "__main__":
    Engine().run()


# End File: cver/src/cver/ingest/download_images.py
