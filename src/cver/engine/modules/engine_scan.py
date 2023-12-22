"""
    Cver Engine
    Scan

"""
import logging

from cver.client.collections.image_build_waitings import ImageBuildWaitings
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.engine.modules.image_scan import ImageScan
from cver.engine.utils import glow


class EngineScan:

    def __init__(self):
        self.scan_limit = glow.engine_info["scan_limit"]
        self.process_limit = glow.engine_info["scan_process_limit"]
        self.fail_threshold = glow.engine_info["scan_fail_threshold"]
        self.scanned = 0
        self.processed = 0
        self.run_once = False
        self.attemped_ibws = {}
        self.scanned_images_success = []
        self.scanned_images_failed = []
        self.data = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
            "status": None
        }

    def run(self):
        """Primary entrypoint for Engine Scan."""
        logging.info("Running Engine Scan")
        ibws = self.get_image_build_waitings()
        logging.info("Found %s" % len(ibws))
        self.handle_scans(ibws)
        logging.info("Scan process complete!")
        ret = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
        }
        return ret

    def get_image_build_waitings(self) -> list:
        """Iterate through all the pages of ImageBuildWaitings that are waiting for a scan
        operation to happen.
        """
        ibw_collect = ImageBuildWaitings()
        args = {
            "query": True,
            "fields": {
                "waiting_for": "scan",
            },
            "order_by": {
                "field": "created_ts",
                "direction": "ASC"
            },
            "page": 1
        }
        ibw_collect.get(args)
        ret_ibws = []
        response_json = ibw_collect.response_last_json
        current_page = 1
        last_page = response_json["info"]["last_page"]
        logging.info("Query returned %s Image Build Waitings for scan" % (
            response_json["info"]["total_objects"]))
        while current_page <= last_page:
            logging.info("Working page: %s" % current_page)
            args["page"] = current_page
            ibws = ibw_collect.get(args)
            ret_ibws = ret_ibws + ibws
            current_page = current_page + 1
        logging.info("Collected %s Image Builds Waiting for scan" % len(ret_ibws))
        return ret_ibws

    def handle_scans(self, ibws: list) -> bool:
        """Scan handler. Here we assume we have a set of IBWs prepped and ready to scan."""
        if not ibws:
            logging.info("No Image Builds waiting for scan")
            return True

        if self.processed == self.process_limit:
            logging.info("Hit max ammount of IBW processing.")
            return True

        for ibw in ibws:
            if ibw.fail_count and ibw.fail_count > self.fail_threshold:
                logging.info("Skipping IBW: %s, fail count (%s) above threshold (%s)." % (
                    ibw,
                    ibw.fail_count,
                    self.fail_threshold))
                continue

            self.processed += 1
            if self.processed > self.process_limit:
                logging.info("Hit max ammount of IBW processing.")
                self.processed = self.processed - 1
                return True
            logging.info("Processing %s - %s of %s" % (
                ibw,
                self.processed, self.process_limit))
            image_scanned = ImageScan(ibw=ibw).run()
            if image_scanned["status"]:
                self.scanned += 1
                self.scanned_images_success.append(image_scanned["image"])
            else:
                self.scanned_images_failed.append(image_scanned["image"])

            if self.scanned >= self.scan_limit:
                logging.info("Completed %s of %s scans" % (
                    self.scanned,
                    self.scan_limit))
                break

        if self.run_once:
            return True
        self.data["status"] = True
        return True

    def get_image_build_waiting_specific(self):
        self.scan_limit = 1
        self.run_once = True
        ib = ImageBuildWaiting()
        if not ib.get_by_id(48):
            logging.info("Image Build Waiting not found!")
            return []
        return [ib]

# End File: cver/src/cver/engine/modules/engine_scan.py
