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


def run_trivy(image: Image, ib: ImageBuild) -> str:
    cmd = get_trivy_cmd(image, ib)
    if not cmd:
        logging.error("Cannot run scan for: %s" % ib)
        return False
    scan_result_raw = subprocess.check_output(cmd)
    scan_result = json.loads(scan_result_raw)
    return scan_result


def get_trivy_cmd(image: Image, ib: ImageBuild) -> str:
    """
    """
    image_loc = ""
    if ib.repository_imported:
        logging.warning("Using TAG for scan, not sha!")
        image_loc = "%s/%s:%s" % (ib.repository_imported, image.name, ib.tags[0])
    else:
        logging.error("No repository imported to use for %s" % ib)
        return False
    cmd = ["trivy", "image", "--scanners", "vuln", "--format", "json", "--quiet", image_loc]
    return cmd

# End File: cver/src/cver/engine/utils/scan.py
