"""
    Cver Shared
    Utils - Docker
    Utilities for interacting with docker

"""
import logging
import subprocess


def pull_image(image_loc: str, pull_through_registry: str = None) -> bool:
    """Download the docker image.
    @note: For now we'll assume we always have a pull through cache like Harbor available.
    """
    if pull_through_registry:
        image_pull_loc = "%s/%s" % (pull_through_registry, image_loc)
    else:
        image_pull_loc = image_loc

    pull_cmd = ["docker", "pull", image_loc]
    image_pull = subprocess.check_output(pull_cmd).decode("utf-8")
    pull_status = image_pull[image_pull.find("Status:"):]
    logging.info("Pull status for %s: %s" % (image_pull_loc, pull_status))
    return True


def get_image_sha(image: str) -> str:
    """Get a docker image's full sha from the image name, including the full registry location.
    :param image: The image to get the full sha from
        example: harbor.squid-ink.us/docker-hub/emby/embyserver
    """
    cmd = ["docker", "inspect", "--format='{{.RepoDigests}}'", image]
    image_details = subprocess.check_output(cmd)
    if not image_details:
        logging.error("Failed to get image sha for %s" % image)
        return False

    image_details = image_details.decode("utf-8")
    print(image_details)
    if "@sha256:" not in image_details:
        logging.error("Could not get image sha from docker")
        return False
    sha = image_details[image_details.find("@sha256:") + 8:image_details.find(" ")]
    return sha


# End File: cver/src/shared/utils/docker.py
