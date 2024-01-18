"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine job.
    This service is intended to run as a cronjob on the Kubernetes system. 
    It's responsibilities are
    -

"""
import logging

from cver.client.models.image_build import ImageBuild
from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.image_build_waitings import ImageBuildWaitings
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.shared.utils import date_utils
from cver.engine.modules.image_download import ImageDownload
from cver.engine.utils import glow


class EngineDownload:

    def __init__(self):
        self.download_limit = glow.engine_info["download_limit"]
        self.process_limit = glow.engine_info["download_process_limit"]
        self.downloaded = 0
        self.processed = 0
        self.api_ibws = {}
        self.api_ibws_current_page = 0
        self.downloaded_images_success = []
        self.downloaded_images_failed = []

    def run(self):
        """Primary entrypoint for Cver Egnine Download."""
        logging.info("Running Engine Download")
        self.set_ibws()
        self.handle_downloads()
        logging.info("Download process complete!")
        ret = {
            "downloaded": self.downloaded,
            "download_limit": self.download_limit,
            "proccessed_ibws": self.processed,
            "downloaded_images_success": self.downloaded_images_success,
            "downloaded_images_failed": self.downloaded_images_failed,
            "status": None
        }
        return ret

    def set_ibws(self) -> bool:
        """Creating IBWs for ImageBuilds that are ready for the download process. Here we will
        create as many IBWs as possible, even though it's likely we'll be restricting the download
        ammount.
        """
        ib_collect = ImageBuilds()
        args = {
            "query": True,
            "order_by": {
                "field": "sync_last_ts",
                "direction": "ASC"
            },
            "page": 1
        }
        ibs = ib_collect.get(args)
        response_json = ib_collect.response_last_json
        current_page = response_json["info"]["current_page"]
        last_page = response_json["info"]["last_page"]
        ibws_created = 0
        logging.info("Found %s potential ImageBuilds to create IBWs from" % len(ibs))
        ibws_created = 0
        while current_page <= last_page:
            logging.info("Working on page %s of %s Image Builds" % (current_page, last_page))
            args["page"] = current_page
            ibs = ib_collect.get(args)
            created = self._handle_ibws_create(ibs)
            ibws_created = ibws_created + created
            current_page += 1

        logging.info("Completed IBW create")
        logging.info("Created %s IBWs" % ibws_created)
        return True

    def handle_downloads(self):
        """Handle all downloads, fetching working to do and kicking off the individual download
        processes.
        """
        ibws = self.get_image_build_waitings()

        if self.processed == self.process_limit:
            logging.info("Hit max ammount of IBW processing.")
            return True
        fail_threshold = 1

        for ibw in ibws:
            if ibw.fail_count and ibw.fail_count > fail_threshold:
                logging.info("Skipping IBW: %s, fail count (%s) above threshold (%s)." % (
                    ibw,
                    ibw.fail_count,
                    fail_threshold))
                continue
            self.processed += 1
            if self.processed > self.process_limit:
                logging.info("Hit max ammount of IBW processing.")
                self.processed = self.processed - 1
                return True
            logging.info("Processing %s of %s" % (self.processed, self.process_limit))
            image_download = ImageDownload(ibw=ibw).run()
            if image_download["status"]:
                self.downloaded += 1
                self.downloaded_images_success.append(image_download["image"])
            else:
                self.downloaded_images_failed.append(image_download["image"])

            if self.downloaded >= self.download_limit:
                logging.info("Completed %s of %s downloads" % (
                    self.downloaded,
                    self.download_limit))
                break

        # if self.downloaded < self.download_limit:
        #     self.handle_downloads()

        return True

    def get_image_build_waitings(self):
        self.api_ibws_current_page += 1
        ibw_collect = ImageBuildWaitings()
        the_args = {
            "query": True,
            "fields": {
                "waiting_for": "download"
            },
            "order_by": {
                "field": "created_ts",
                "direction": "ASC"
            },
            "page": self.api_ibws_current_page
        }
        ibws = ibw_collect.get(the_args)

        self.api_ibws = ibw_collect.response_last_json["info"]
        if self.api_ibws_current_page == 1:
            logging.info("Found %s Image Builds waiting for download" % (
                self.api_ibws["total_objects"]))
        else:
            logging.info("Got page %s of %s of ImageBuilds waiting for download" % (
                self.api_ibws_current_page,
                self.api_ibws["last_page"]))
        return ibws

    def _handle_ibws_create(self, ibs: list) -> int:
        """Handles the cration of ImageBuildWaitings from a list of ImageBuilds.
        """
        ibws_created = 0
        for ib in ibs:
            if self._handle_ibw_create(ib):
                ibws_created += 1
        return ibws_created

    def _handle_ibw_create(self, ib: ImageBuild) -> bool:
        """Handles the creation of a single ImageBuildWaiting, as well as Registry records that
        need to be created.
        """
        if not date_utils.interval_ready(ib.sync_last_ts, 96):
            logging.info("%s: Not flagging image build for sync" % ib)
            return False

        ibw = ImageBuildWaiting()
        ibw.sha = ib.sha
        if ibw.get_by_sha():
            logging.debug("IBW already exists, not creating. %s" % ibw)
            return False

        ibw.image_id = ib.image_id
        ibw.image_build_id = ib.id
        ibw.registry_id = ib.registry_id
        if len(ib.tags) > 0:
            ibw.tag = ib.tags[0]
        ibw.waiting_for = "download"
        ibw.waiting = True
        if ibw.save():
            logging.info("%s: Saved" % ibw)
            return True
        else:
            logging.error("%s: Failed to save" % ibw)
            return False

# End File: cver/src/cver/engine/modules/engine-download.py
