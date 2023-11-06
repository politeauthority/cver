"""
    Cver Engine
    Utils
    Scan
        Utlities for docker image scanning

"""
import json
import logging
import subprocess


def run_trivy(local_image_location: str) -> str:
    cmd = [
        "trivy",
        "image",
        "--scanners",
        "vuln",
        "--format",
        "json",
        "--quiet",
        local_image_location]
    try:
        logging.info("\n\nSCAN CMD\n%s" % " ".join(cmd))
        scan_result_raw = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logging.error("Error running command\n\t%s\n%s" % (" ".join(cmd), e))
        return False
    scan_result = json.loads(scan_result_raw)
    return scan_result


# def get_trivy_cmd(image: Image, ib: ImageBuild) -> str:
#     """
#     """
#     image_loc = ""
#     if ib.registry_imported:
#         pull_thru_loc = ""
#         if ib.registry in glow.registry_info["pull_thrus"]:
#             pull_thru_loc = "%s/" % glow.registry_info["pull_thrus"][ib.registry]

#         logging.info("Using registry imported for %s - %s" % (image, ib))
#         logging.warning("Using TAG for scan, not sha!")
#         image_loc = "%s/%s%s:%s" % (ib.registry_imported, pull_thru_loc, image.name, ib.tags[0])
#     else:
#         logging.error("No registry imported to use for %s from %s" % (ib, image.registry))
#         return False
#     cmd = ["trivy", "image", "--scanners", "vuln", "--format", "json", "--quiet", image_loc]
#     logging.info("TRIVY SCAN CMD: %s" % " ".join(cmd))
#     return cmd

# End File: cver/src/cver/engine/utils/scan.py
