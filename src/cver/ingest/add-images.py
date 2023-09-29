"""
    Cver Ingest
    Add Images
    Clunky tool for adding Images through the Cver Api

"""
import logging

from cver.shared.utils import docker
# from cver.cver_client import CverClient
from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting


class AddImages:

    def run(self):
        static_images = self.get_static_images()
        # local_images = self.get_local_images()
        images = []
        images += static_images
        self.submit_images(images)

    def get_static_images(self):
        emby = {
            "name": "emby/embyserver",
            "tag": "latest",
        }
        images = [emby]
        return images

    def get_local_images(self) -> list:
        """Get local images from the Docker host, currently pruning them down to just a few specific
        repos.
        """
        local_images = docker.get_local_images()
        images_to_select = [
            # "mysql",
            # "aquasec/trivy",
            # "kennethreitz/httpbin",
            "wordpress"
        ]
        images_to_use = []
        for image in local_images:
            if image["name"] in images_to_select:
                images_to_use.append(image)
        logging.info("Found %s of %s Docker images to submit" % (
            len(images_to_use), len(local_images)))
        return images_to_use

    def submit_images(self, the_images: list) -> bool:
        """Submit a list of raw Image data to Cver, creating Images and ImageBuilds."""
        for the_image in the_images:
            if "sha" not in the_image and "tag" not in the_image:
                logging.error("Image needs a sha or tag to submit: %s" % the_image["name"])
                continue

            image = Image()
            image.name = the_image["name"]
            if "repository" not in the_image:
                image.repository = "docker.io"
            else:
                image.repository = the_image["repository"]
            image.save()
            logging.info("\tWrote: %s" % image)
            # If we have data to create an ImageBuild
            if "sha" in the_image:
                image_build = ImageBuild()
                image_build.sha = the_image["sha"]
                image_build.image_id = image.id
                image_build.repository = image.repository
                image_build.tags = [the_image["tag"]]
                image_build.save()
                logging.info("\tWrote: %s" % image_build)
            else:
                self.submit_image_build_waiting(image, the_image["tag"])
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
        ibw.tag = tag
        ibw.waiting_for = "download"
        if ibw.save():
            return True
        else:
            return False


if __name__ == "__main__":
    AddImages().run()


# End File: cver/src/cver/ingest/add_images.py
