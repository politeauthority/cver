"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system 

"""
import logging

# from cver.ingest.utils import docker
# from cver.cver_client import CverClient
from cver.cver_client.models.image import Image
# from cver.cver_client.models.image_build import ImageBuild
# from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.option import Option


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
        """Check that have a registry to push to."""
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

        return True

    def get_image_build_waitings(self):
        """Get the ImageBuildsWaiting for some sort of processing."""
        ibws = ImageBuildWaitings().get()
        return ibws

    def determine_work(self, ibw):
        image = Image()
        image.get_by_id(ibw.image_id)
        # if ibw.image_build_id:



if __name__ == "__main__":
    Engine().run()


# End File: cver/src/cver/ingest/download_images.py
