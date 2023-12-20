"""
    Cver Engine
    Utils
    Scan
        Utlities for docker image scanning

"""
import json
import logging
import subprocess

from cver.shared.utils import misc


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


def parse_trivy(scan_result: dict) -> dict:
    """Parse the dictionary coming from Trivy into a simplified result that will apply to a Cver
    Scan model.
    """
    ret = {
        "cve_critical_int": 0,
        "cve_critical_nums": [],
        "cve_high_int": 0,
        "cve_high_nums": [],
        "cve_medium_int": 0,
        "cve_medium_nums": [],
        "cve_low_int": 0,
        "cve_low_nums": [],
        "cve_unknown_int": 0,
        "cve_unknown_nums": [],
    }
    vulns = misc.get_dict_path(scan_result, "Results.0.Vulnerabilities")
    if not vulns:
        # import ipdb; ipdb.set_trace()
        logging.error("Unable to read vulnerability data from scan.")
        return False
    # vulns = scan_result["Results"][0]["Vulnerabilities"]
    for vuln in vulns:
        cve_num = vuln["VulnerabilityID"]
        cve_sev = vuln["Severity"]
        if cve_sev == "CRITICAL":
            if cve_num not in ret["cve_critical_nums"]:
                ret["cve_critical_int"] += 1
                ret["cve_critical_nums"].append(cve_num)
        elif cve_sev == "HIGH":
            if cve_num not in ret["cve_high_nums"]:
                ret["cve_high_int"] += 1
                ret["cve_medium_nums"].append(cve_num)
        elif cve_sev == "MEDIUM":
            if cve_num not in ret["cve_medium_nums"]:
                ret["cve_medium_int"] += 1
                ret["cve_medium_nums"].append(cve_num)
        elif cve_sev == "LOW":
            if cve_num not in ret["cve_low_nums"]:
                ret["cve_low_int"] += 1
                ret["cve_unknown_nums"].append(cve_num)
        elif cve_sev == "UNKNOWN":
            if cve_num not in ret["cve_unknown_nums"]:
                ret["cve_unknown_int"] += 1
                ret["cve_unknown_nums"].append(cve_num)
        else:
            logging.warning("Uknown CVE severity: %s\n%s" % (cve_sev, vuln))
    return ret

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
