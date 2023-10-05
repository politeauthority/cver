"""
    Cver Shared
    Utils
    Misc
    A bunch of misc tools to share between efforts.

"""
import logging
import json
import re
import pprint

import tldextract


def container_url(the_string: str):
    """Break down a container url into its parts.
    :unit-test: test__container_url
    """
    ret = {
        "repository": _get_repository(the_string),
        "image": None,
        "tag": _get_tag(the_string),
        "sha": _get_sha(the_string),
        "full": None,
        "og": the_string
    }
    ret["image"] = _get_image(the_string, ret["repository"])
    ret["full"] = _get_full(ret)
    return ret


def is_fqdn(hostname: str) -> bool:
    """Check if a string is a FQDN.
    :unit-test: test__is_fqdn
    """
    if not 1 < len(hostname) < 253:
        return False
    if hostname[-1] == '.':
        hostname = hostname[0:-1]
    labels = hostname.split('.')
    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)
    return all(fqdn.match(label) for label in labels)


def strip_trailing_slash(the_string: str) -> str:
    """Strips trailing slashes if they exist."""
    if not the_string:
        return the_string
    if the_string[-1:] == "/":
        return the_string[:-1]
    return the_string


def dict_to_json(the_dict: dict, file_name: str) -> bool:
    """Save a Python dictionary to a json file on the filesystem."""
    with open(file_name, "w") as fp:
        json.dump(the_dict, fp)
    return True


def pretty_print(data):
    pprint.pprint(data)
    return True


def _get_image(the_string: str, registry: str = None) -> str:
    """Seprate the image from the docker container url.
    """
    if registry:
        registry += "/"
        the_string = the_string.replace(registry, "")
    if ":" in the_string:
        find_colon = the_string.find(":")
        the_string = the_string[:find_colon]
    if "@" in the_string:
        find_at = the_string.find("@")
        the_string = the_string[:find_at]
    return the_string


def _get_repository(the_string: str) -> str:
    """Get the repository from the container url.
    :unit-test: test___get_repository
    """
    default_repository = "docker.io"
    extracted = tldextract.extract(the_string)
    if not extracted.suffix:
        return default_repository
    tld_len = len(extracted.suffix)
    repository = the_string[:the_string.find(extracted.suffix) + tld_len]
    return repository


def _get_tag(the_string: str) -> str:
    """Gets the tag, if present, of a Docker image location string.
    :unit-test: test___get_tag
    """
    num_colons = the_string.count(":")
    if num_colons == 0:
        logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
        return "latest"
    elif num_colons == 1:
        if "@" in the_string:
            logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
            return "latest"
        tag_loc = the_string.find(":")
        tag = the_string[tag_loc + 1:]
    elif num_colons == 2:
        if "@" not in the_string:
            logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
            return "latest"
        tag_loc_first = the_string.find(":")
        tag_loc_last = the_string.find("@")
        tag = the_string[tag_loc_first + 1: tag_loc_last]

    return tag


def _get_sha(the_string: str) -> str:
    """Gets the sha, if present, of a Docker image location string.
    :unit-test: test__get_sha
    """
    if "@sha256:" not in the_string:
        return ""
    sha_loc = the_string.find("@")
    sha = the_string[sha_loc + 8:]
    return sha


def _get_full(the_image_url: dict):
    """Get a full docker image url from its pieces.
    :unit-test: test__get_full
    """
    the_url = the_image_url["repository"]
    the_url += "/" + the_image_url["image"]
    if the_image_url["tag"] or the_image_url["sha"]:
        the_url += ":"
        if the_image_url["tag"]:
            the_url += the_image_url["tag"]
        if the_image_url["sha"]:
            the_url += ":@%s" % the_image_url["sha"]
    return the_url


# End File: cver/src/shared/utils/misc.py
