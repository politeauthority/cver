"""
    Cver Shared
    Utils
    Misc
    A bunch of misc tools to share between efforts.

"""
# import logging
import json
import re
import pprint

import glom
import tldextract


def container_url(the_string: str):
    """Break down a container url into its parts.
    :unit-test: TestSharedUtilMisc::test__container_url
    """
    ret = {
        "registry": _get_registry(the_string),
        "image": None,
        "tag": _get_tag(the_string),
        "sha": _get_sha(the_string),
        "full": None,
        "og": the_string
    }
    ret["image"] = _get_image(the_string, ret["registry"])
    ret["full"] = _get_full(ret)
    return ret


def is_fqdn(hostname: str) -> bool:
    """Check if a string is a FQDN.
    :unit-test: TestSharedUtilMisc::test__is_fqdn
    """
    if not 1 < len(hostname) < 253:
        return False
    if hostname[-1] == '.':
        hostname = hostname[0:-1]
    labels = hostname.split('.')
    fqdn = re.compile(r'^[a-z0-9]([a-z-0-9-]{0,61}[a-z0-9])?$', re.IGNORECASE)
    return all(fqdn.match(label) for label in labels)


def percentize(part: int, whole: int, round_int: int = 1) -> float:
    """Get the percent value that a part is from a whole.
    :unit-test: TestSharedUtilMisc:: test__percentize
    """
    if part == 0 or whole == 0:
        return 0
    per = (part * 100) / whole
    per = round(per, round_int)
    return per


def strip_trailing_slash(the_string: str) -> str:
    """Strips trailing slashes if they exist.
    :unit-test: TestSharedUtilMisc::test__strip_trailing_slash
    """
    if not the_string:
        return the_string
    if the_string[-1:] == "/":
        return the_string[:-1]
    return the_string


def add_trailing_slash(the_string: str) -> str:
    """Adds a trailing slash if one does not exist.
    :unit-test: TestSharedUtilMisc::test__add_trailing_slash
    """
    if not the_string:
        return the_string
    if the_string[-1:] == "/":
        return the_string
    return the_string + "/"


def dict_to_json(the_dict: dict, file_name: str) -> bool:
    """Save a Python dictionary to a json file on the filesystem."""
    with open(file_name, "w") as fp:
        json.dump(the_dict, fp)
    return True


def get_dict_path(the_dict: dict, the_path: str):
    try:
        found = glom.glom(the_dict, the_path)
    except glom.core.PathAccessError:
        return False
    return found


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


def _get_registry(the_string: str) -> str:
    """Get the registry from the container url.
    :unit-test: test__get_registry
    """
    default_registry = "docker.io"
    extracted = tldextract.extract(the_string)
    if not extracted.suffix:
        return default_registry
    tld_len = len(extracted.suffix)
    registry = the_string[:the_string.find(extracted.suffix) + tld_len]
    return registry


def _get_tag(the_string: str) -> str:
    """Gets the tag, if present, of a Docker image location string.
    :unit-test: test___get_tag
    """
    num_colons = the_string.count(":")
    if num_colons == 0:
        # logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
        return "latest"
    elif num_colons == 1:
        if "@" in the_string:
            # logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
            return "latest"
        tag_loc = the_string.find(":")
        tag = the_string[tag_loc + 1:]
    elif num_colons == 2:
        if "@" not in the_string:
            # logging.debug("Cant get tag from string: '%s' assuming 'latest'" % the_string)
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
    the_url = the_image_url["registry"]
    the_url += "/" + the_image_url["image"]
    if the_image_url["tag"] or the_image_url["sha"]:
        the_url += ":"
        if the_image_url["tag"]:
            the_url += the_image_url["tag"]
        if the_image_url["sha"]:
            the_url += ":@%s" % the_image_url["sha"]
    return the_url


# End File: cver/src/shared/utils/misc.py
