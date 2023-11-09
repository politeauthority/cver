"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system.

"""
import logging

from cver.client.collections.image_builds import ImageBuilds
from cver.client.collections.image_build_waitings import ImageBuildWaitings
from cver.client.models.image_build_waiting import ImageBuildWaiting
from cver.shared.utils import date_utils
from cver.engine.modules.image_download import ImageDownload
from cver.engine.utils import glow


class EngineDownload:

    def __init__(self):
        # @todo: Make CVER_ENGINE_DOWNLOAD_LIMIT derived from an option value
        # @todo: Make this pulled through options/ allow non pull throughs
        self.download_limit = glow.engine_info["download_limit"]
        self.process_limit = glow.engine_info["download_process_limit"]
        self.downloaded = 0
        self.processed = 0
        self.api_ibws = {}
        self.api_ibws_current_page = 0
        self.downloaded_images_success = []
        self.downloaded_images_failed = []

    def run(self):
        """Primary entrypoint for Cver Egnine Download.
        """
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
        """Creating IBWs for ImageBuilds that are ready for the download process."""
        ib_col = ImageBuilds()
        args = {
            "fields": {
                "sync_enabled": True
            },
            "order_by": {
                "field": "sync_last_ts",
                "direction": "ASC"
            },
            "limit": 1
        }
        ibs = ib_col.get(args)
        ibws_created = 0
        for ib in ibs:
            if date_utils.interval_ready(ib.sync_last_ts, 96):
                logging.debug("%s: Not flagging image build for sync" % ib)
                continue
            ibw = ImageBuildWaiting()
            ibw.image_id = ib.image_id
            ibw.image_build_id = ib.id
            ibw.sha = ib.sha
            if len(ib.tags) > 0:
                ibw.tag = ib.tags[0]
            ibw.waiting_for = "download"
            ibw.waiting = True
            if ibw.save():
                logging.info("%s: Saved" % ibw)
                ibws_created += 0
            else:
                logging.error("%s: Failed to save" % ibw)

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

        for ibw in ibws:
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
        self.api_ibws = ibw_collect.response_last["info"]
        if self.api_ibws_current_page == 1:
            logging.info("Found %s Image Builds waiting for download" % (
                self.api_ibws["total_objects"]))
        else:
            logging.info("Got page %s of %s of ImageBuilds waiting for download" % (
                self.api_ibws_current_page,
                self.api_ibws["last_page"]))
        return ibws


# End File: cver/src/cver/engine/modules/engine-download.py
