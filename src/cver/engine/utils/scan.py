"""
    Cver Engine
    Utils
    Scan
        Utlities for docker image scanning

"""
import json
import logging
import subprocess

from cver.cver_client.models.image import Image
from cver.cver_client.models.image_build import ImageBuild
from cver.engine.utils import glow


def run_trivy(image: Image, ib: ImageBuild) -> str:
    cmd = get_trivy_cmd(image, ib)
    import ipdb; ipdb.set_trace()
    if not cmd:
        logging.error("Cannot run scan for: %s" % ib)
        return False
    try:
        logging.info("\n\nSCAN CMD\n%s" % " ".join(cmd))
        scan_result_raw = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.error("Error running command\n\t%s\n%s" % (" ".join(cmd), e))
        return False
    scan_result = json.loads(scan_result_raw)
    return scan_result


def get_trivy_cmd(image: Image, ib: ImageBuild) -> str:
    """
    """
    image_loc = ""
    if ib.registry_imported:
        pull_thru_loc = ""
        if ib.registry in glow.registry_info["pull_thrus"]:
            pull_thru_loc = "%s/" % glow.registry_info["pull_thrus"][ib.registry]

        logging.info("Using registry imported for %s - %s" % (image, ib))
        logging.warning("Using TAG for scan, not sha!")
        image_loc = "%s/%s%s:%s" % (ib.registry_imported, pull_thru_loc, image.name, ib.tags[0])
    else:
        logging.error("No registry imported to use for %s from %s" % (ib, image.registry))
        return False
    cmd = ["trivy", "image", "--scanners", "vuln", "--format", "json", "--quiet", image_loc]
    return cmd

# End File: cver/src/cver/engine/utils/scan.py
