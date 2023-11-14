"""
    Cver Engine
    Scan

"""
import logging

from cver.shared.utils import date_utils
from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.image_build_waitings import ImageBuildWaitings
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.engine.modules.image_scan import ImageScan
from cver.engine.utils import glow


class EngineScan:

    def __init__(self):
        self.scan_limit = glow.engine_info["scan_limit"]
        self.process_limit = glow.engine_info["scan_process_limit"]
        self.scanned = 0
        self.api_ibws = {}
        self.api_ibws_current_page = 0
        self.processed = 0
        self.fail_threshold = 3
        self.registry_pull_thru_docker_io = None
        self.run_once = False
        self.attemped_ibws = {}
        self.scanned_images_success = []
        self.scanned_images_failed = []
        self.scan_tasks = {}
        self.data = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
            "scan_tasks": self.scan_tasks,
            "status": None
        }

    def run(self):
        logging.info("Running Engine Scan")
        self.set_ibws()
        self.handle_scans()
        logging.info("Scan process complete!")
        ret = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
        }
        return ret

    def set_ibws(self) -> bool:
        """Creating IBWs for ImageBuilds that are ready for the download process."""
        ib_col = ImageBuilds()
        args = {
            "fields": {
                "scan_enabled": True
            },
            "order_by": {
                "field": "scan_last_ts",
                "direction": "ASC"
            },
            "limit": 1
        }
        ibs = ib_col.get(args)
        ibws_created = 0
        scan_interval_hours = glow.engine_info["engine_download_interval"]
        for ib in ibs:
            if not date_utils.interval_ready(ib.scan_last_ts, scan_interval_hours):
                logging.debug("%s: Not flagging image build for sync" % ib)
                continue
            ibw = ImageBuildWaiting()
            ibw.image_id = ib.image_id
            ibw.image_build_id = ib.id
            ibw.sha = ib.sha
            if len(ib.tags) > 0:
                ibw.tag = ib.tags[0]
            ibw.waiting_for = "scan"
            ibw.waiting = True
            if ibw.save():
                logging.info("%s: Saved" % ibw)
                ibws_created += 0
            else:
                logging.error("%s: Failed to save" % ibw)

        logging.info("Created %s IBWs" % ibws_created)
        return True

    def handle_scans(self) -> bool:
        ibws = self.get_image_build_waitings()
        logging.info("Found %s" % len(ibws))
        if not ibws:
            logging.info("No Image Builds waiting for scan")
            return True

        if self.processed == self.process_limit:
            logging.info("Hit max ammount of IBW processing.")
            return True

        for ibw in ibws:
            self.processed += 1
            if self.processed > self.process_limit:
                logging.info("Hit max ammount of IBW processing.")
                self.processed = self.processed - 1
                return True
            logging.info("Processing %s of %s" % (self.processed, self.process_limit))
            image_scanned = ImageScan(ibw=ibw).run()
            if image_scanned["status"]:
                self.scanned += 1
                self.scanned_images_success.append(image_scanned["image"])
            else:
                self.scanned_images_failed.append(image_scanned["image"])

            # Handle Scan Process that happen reguardless
            self.scan_tasks[self.ib.id] = image_scanned["task"]

            if self.scanned >= self.scan_limit:
                logging.info("Completed %s of %s scans" % (
                    self.scanned,
                    self.scan_limit))
                break

        if self.run_once:
            return True

        # if self.scanned < self.scan_limit:
        #     self.handle_scans()
        self.data["status"] = True
        return True

    def get_image_build_waitings(self) -> list:
        self.api_ibws_current_page += 1
        ibw_collect = ImageBuildWaitings()

        if "last_page" in self.api_ibws:
            if self.api_ibws_current_page > self.api_ibws["last_page"]:
                logging.info("At the end of ImageBuild's Waiting for scan.")
                return []
        the_args = {
            "query": True,
            "fields": {
                "waiting_for": "scan",
            },
            "order_by": {
                "field": "created_ts",
                "direction": "ASC"
            },
            "page": self.api_ibws_current_page
        }
        ibws = ibw_collect.get(the_args)
        self.api_ibws = ibw_collect.response_last["info"]
        # if self.api_ibws_current_page == 1:
        #     logging.info("Found %s Image Builds waiting for scan" % (
        #         self.api_ibws["total_objects"]))
        # else:
        #     logging.info("Got page %s of %s of ImageBuilds waiting for scan" % (
        #         self.api_ibws_current_page,
        #         self.api_ibws["last_page"]))
        # new_ibws = []
        # for ibw in ibws:
        #     if ibw.id not in self.attemped_ibws:
        #         new_ibws.append(ibw)
        return ibws

    def get_image_build_waiting_specific(self):
        self.scan_limit = 1
        self.run_once = True
        ib = ImageBuildWaiting()
        if not ib.get_by_id(48):
            logging.info("Image Build Waiting not found!")
            return []
        return [ib]

# End File: cver/src/cver/engine/modules/engine_scan.py
