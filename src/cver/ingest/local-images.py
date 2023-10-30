"""
    Cver Ingest
    Local Images
    This tool will collect local Docker images and submit them to Cver, to be further analyized.

"""
import logging

from cver.shared.utils import docker
from cver.shared.utils import xlate
# from cver.cver_client import CverClient
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting


class LocalImages:

    def __init__(self):
        self.images_subbmited = 0
        self.images_subbmited_success = 0
        self.images_subbmited_failed = 0

    def run(self):
        images = []
        static_images = self.get_static_images()
        images += static_images
        # local_images = self.get_local_images()
        # images = local_images
        import ipdb; ipdb.set_trace()
        self.submit_images(images)

    def get_static_images(self):
        emby = {
            "name": "emby/embyserver",
            "tag": "latest",
            "sha": "4986a592b5c438b6b6d0193d8acfae021eb4b1bc3ff5abd78b31ad86367fe0d2"
        }
        images = [emby]
        return images

    def get_local_images(self) -> list:
        """Get local images from the Docker host, currently pruning them down to just a few specific
        repos.
        """
        local_images = docker.get_local_images()
        logging.info("Prepairing to submit %s images to Cver" % len(local_images))
        # images_to_select = ["mysql", "aquasec/trivy", "kennethreitz/httpbin", "wordpress"]
        images_to_use = []
        for image in local_images:
            images_to_use.append(image)
        logging.info("Found %s of %s Docker images to submit" % (
            len(images_to_use), len(local_images)))
        return images_to_use

    def submit_images(self, the_images: list) -> bool:
        """Submit a list of raw Image data to Cver, creating Images and ImageBuilds."""
        submmited_ib = 0
        submmited_ibw = 0
        for the_image in the_images:
            if "sha" not in the_image and "tag" not in the_image:
                logging.error("Image needs a sha or tag to submit: %s" % the_image["name"])
                continue

            image = Image()
            image.name = the_image["name"]
            if "registry" not in the_image:
                image.registry = "docker.io"
            else:
                image.registry = the_image["registry"]
            image.save()
            logging.info("\tWrote: %s" % image)

            # If we have data to create an ImageBuild
            if "sha" in the_image:
                image_build = ImageBuild()
                image_build.sha = xlate.get_digest(the_image["sha"])
                image_build.image_id = image.id
                image_build.registry = image.registry
                image_build.tags = [the_image["tag"]]
                image_build.save()
                logging.info("\tWrote: %s" % image_build)
                submmited_ib += 1
            else:
                self.submit_image_build_waiting(image, the_image["tag"])
                submmited_ibw += 1
            logging.info("Submmited %s Image Builds" % submmited_ib)
            logging.info("Submmited %s Image Build Waitings" % submmited_ibw)
        return True

    def submit_image_build_waiting(self, image: Image, tag: str) -> bool:
        """If we dont have an exact sha to work with, we will have to find a relevant one. So we
        store it as ImageBuildWaiting.
        """
        if not image.id:
            logging.error(f"Image missing ID: {image}")
            return False
        ibw = ImageBuildWaiting()
        ibw.image_id = image.id
        ibw.waiting_for = "download"
        ibw.tag = tag
        if ibw.save():
            return True
        else:
            return False


if __name__ == "__main__":
    LocalImages().run()


# End File: cver/src/cver/ingest/local-images.py
