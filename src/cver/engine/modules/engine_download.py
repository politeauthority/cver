"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine job.
    This service is intended to run as a cronjob on the Kubernetes system.
    It's responsibilities are
    -

"""
import logging

# from cver.client.collections.image_builds import ImageBuilds
from cver.engine.modules.image_download import ImageDownload
from cver.engine.utils import glow


logger = logging.getLogger(__name__)


class EngineDownload:

    def __init__(self):
        self.priority = glow.image_build_priority["download"]
        self.download_limit = glow.engine_info["download_limit"]
        self.process_limit = glow.engine_info["download_process_limit"]
        self.downloaded = 0
        self.processed = 0
        self.downloaded_images_success = []
        self.downloaded_images_failed = []

    def run(self):
        """Primary entrypoint for Cver Egnine Download."""
        logger.info("Running Engine Download")
        msg = "Engine Priorty supplied: %s records, current download limit set to %s with a "
        msg += "process limit of %s"
        msg = msg % (len(self.priority), self.download_limit, self.process_limit)
        logger.info(msg)
        self.handle_downloads()
        logger.info("Download process complete!")
        ret = {
            "downloaded": self.downloaded,
            "download_limit": self.download_limit,
            "proccessed_ibws": self.processed,
            "downloaded_images_success": self.downloaded_images_success,
            "downloaded_images_failed": self.downloaded_images_failed,
            "status": None
        }
        return ret

    def handle_downloads(self):
        """Handle all downloads, fetching working to do and kicking off the individual download
        processes.
        """
        if self.processed == self.process_limit:
            logger.info("Hit max ammount of IBW processing.")
            return True
        # fail_threshold = 1
        for ib_id, priorty_ib in self.priority.items():
            logger.info("Processing image-build: %s %s of %s" % (priorty_ib, self.processed, self.process_limit))
            image_download = ImageDownload(ib=priorty_ib["image_build"]).run()

            if image_download["status_download"]:
                self.downloaded += 1
                self.downloaded_images_success.append(image_download["image"])
            else:
                self.downloaded_images_failed.append(image_download["image"])

        #     if self.downloaded >= self.download_limit:
        #         logger.info("Completed %s of %s downloads" % (
        #             self.downloaded,
        #             self.download_limit))
        #         break

        if self.downloaded < self.download_limit:
            self.handle_downloads()

        return True

# End File: cver/src/cver/engine/modules/engine-download.py
