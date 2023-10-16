"""
    Cver Engine
    Scan

"""
import logging
import os

from cver.cver_client.collections.image_build_waitings import ImageBuildWaitings
from cver.cver_client.models.image_build_waiting import ImageBuildWaiting
from cver.engine.modules.image_scan import ImageScan


class EngineScan:
    def __init__(self):
        self.scan_limit = int(os.environ.get("CVER_ENGINE_SCAN_LIMIT", 1))
        self.scanned = 0
        self.api_ibws = {}
        self.api_ibws_current_page = 0
        self.ibws_processed = 0
        self.fail_threshold = 3
        self.registry_pull_thru_docker_io = None
        self.run_once = False
        self.attemped_ibws = {}
        self.scanned_images_success = []
        self.scanned_images_failed = []
        self.data = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.ibws_processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
            "status": None
        }

    def run(self):
        logging.info("Running Engine Scan")
        self.handle_scans()
        logging.info("Scan process complete!")
        ret = {
            "scanned": self.scanned,
            "scan_limit": self.scan_limit,
            "proccessed_ibws": self.ibws_processed,
            "scanned_images_success": self.scanned_images_success,
            "scanned_images_failed": self.scanned_images_failed,
        }
        return ret

    def handle_scans(self) -> bool:
        ibws = self.get_image_build_waitings()
        logging.info("Found %s" % len(ibws))
        if not ibws:
            logging.info("No Image Builds waiting for scan")
            return True

        if self.ibws_processed > 10:
            return True

        for ibw in ibws:
            if ibw.fail_count >= self.fail_threshold:
                logging.warning("IBW pass fail threshold of %s, has %s: %s" % (
                    self.fail_threshold,
                    ibw.fail_count,
                    ibw))
                continue
            self.ibws_processed += 1
            logging.info("Starting ImageBuild %s waiting. Processing: %s" % (
                self.ibws_processed,
                ibw
            ))
<<<<<<< HEAD
            image_scanned = ImageScan(ibw=ibw).run()
            if image_scanned["status"]:
                self.scanned += 1
                self.scanned_images_success.append(image_scanned["image"])
            else:
                self.scanned_images_failed.append(image_scanned["image"])

            if not image_scanned:
=======
            scanned = ImageScan(ibw=ibw).run()

            if not scanned:
>>>>>>> 34a120d (working on engine-scans)
                logging.warning("Did not complete scan for: %s" % ibw)
                self.attemped_ibws[ibw.id] = ibw
                continue

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
            "waiting_for": "scan",
            "page": self.api_ibws_current_page
        }
        ibws = ibw_collect.get(the_args)
        self.api_ibws = ibw_collect.response_last["info"]
        if self.api_ibws_current_page == 1:
            logging.info("Found %s Image Builds waiting for scan" % (
                self.api_ibws["total_objects"]))
        else:
            logging.info("Got page %s of %s of ImageBuilds waiting for scan" % (
                self.api_ibws_current_page,
                self.api_ibws["last_page"]))
        new_ibws = []
        for ibw in ibws:
            if ibw.id not in self.attemped_ibws:
                new_ibws.append(ibw)
        return new_ibws

    def get_image_build_waiting_specific(self):
        self.scan_limit = 1
        self.run_once = True
        ib = ImageBuildWaiting()
        if not ib.get_by_id(48):
            logging.info("Image Build Waiting not found!")
            return []
        return [ib]

# End File: cver/src/cver/engine/modules/engine_scan.py
