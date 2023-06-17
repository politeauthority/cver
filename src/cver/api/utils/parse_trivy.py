"""
    Cver Api - Util
    Parse Trivy
    Takes the json output of a trivy scan and breaks it into usable parts for a Cver Api Scan model.

"""
import logging


def parse(scan_raw: dict):
    results = scan_raw["Results"]
    parsed = {
        "cve_critical_int": 0,
        "cve_critical_nums": [],
        "cve_high_int": 0,
        "cve_high_nums": [],
        "cve_medium_int": 0,
        "cve_medium_nums": [],
        "cve_low_int": 0,
        "cve_low_nums": [],
    }
    logging.info("Targets Found: %s" % len(results))
    for result in results:
        for target in results:
            if "Vulnerabilities" not in target:
                continue
        vulns = target["Vulnerabilities"]

        for vuln in vulns:
            if vuln["Severity"] == "CRITICAL":
                parsed["cve_critical_int"] += 1
                parsed["cve_critical_nums"].append(vuln["VulnerabilityID"])

            elif vuln["Severity"] == "HIGH":
                parsed["cve_high_int"] += 1
                parsed["cve_high_nums"].append(vuln["VulnerabilityID"])

            elif vuln["Severity"] == "MEDIUM":
                parsed["cve_medium_int"] += 1
                parsed["cve_medium_nums"].append(vuln["VulnerabilityID"])

            elif vuln["Severity"] == "LOW":
                parsed["cve_low_int"] += 1
                parsed["cve_low_nums"].append(vuln["VulnerabilityID"])

        print("Target", target["Target"])
        print("Vulns: %s" % len(vulns))
    return parsed
