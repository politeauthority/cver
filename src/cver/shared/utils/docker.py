"""
    Cver Shared
    Utils
    Docker
    Utilities for interacting with docker

"""
import logging
import subprocess


def registry_login(registry_url: str, registry_user: str, registry_pass: str) -> bool:
    """Login to the registry Cver has been instructed to use."""
    cmd = [
        "echo", registry_pass, "|", "docker", "login", registry_url, "--username",
        registry_user, "--password-stdin"
    ]
    result = subprocess.check_output(cmd)
    if not result:
        logging.error("Error connecting to registry: %s" % registry_url)
        return False
    logging.info("Authenticated to registry: %s" % registry_url)
    return True


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


def get_local_images() -> list:
    """Gets all local docker images on a host, attempting to parse them into something useable.
    @todo: This is fragile, ideally should use the JSON formatter, and only get images pulled from a
    remote host.
    """
    # cmd = ["docker", "images", "--digests", "--format", "'{{json .}}'"]
    cmd = ["docker", "images", "--digests"]

    # Execute the command and capture the output
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True)
    stdout, stderr = process.communicate()

    images = []
    line_no = 0
    for line in stdout.splitlines():
        line_no += 1
        if line_no == 1:
            continue
        # Do something with each line
        split = line.split(" ")
        parts = []
        for seg in split:
            if seg:
                parts.append(seg)

        image = {
            "name": parts[0],
            "tag": parts[1],
            "sha": parts[2]
        }
        images.append(image)
    return images


# End File: cver/src/shared/utils/docker.py
