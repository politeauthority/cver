"""
    Cver Engine
    Engine
    Primary entrypoint to the Cver Engine utility.
    This service is intended to run as a cronjob on the Kubernetes system.

"""
import argparse
import logging
import logging.config

from cver.shared.utils.log_config import log_config
from cver.shared.utils import docker
from cver.client.models.option import Option
from cver.client.collections.registries import Registries
<<<<<<< HEAD

from cver.engine.modules.engine_priority import EnginePriority
=======
>>>>>>> origin/stage
from cver.engine.modules.cluster_presence import ClusterPresence
from cver.engine.modules.engine_download import EngineDownload
from cver.engine.modules.engine_scan import EngineScan
from cver.engine.utils import glow

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Engine:

    def __init__(self, cli_args):
        self.args = cli_args
        self.download_report = {}
        self.scan_report = {}

    def run(self):
        logging.info("Starting Cver Engine")
        if not self.preflight():
            logging.critical("Pre flight checks failed.")
            exit(1)

        self.run_cluster_presence()

        if self.args.action in ["all", "download"]:
            self.create_priority(the_phase="download")
            self.run_downloads()
        if self.args.action in ["all", "scan"]:
            self.run_scans()
        if self.args.action in ["all"]:
            self.run_cleanup()
        logging.info("Engine Process Complete")
        msg = "\n\nEngine\n"
        msg += self._draw_download_report()
        msg += self._draw_scan_report()
        logging.info(msg)
        return True

    def preflight(self):
        """Check that have a registry to push/pull to/from."""
        self._get_registries()

        reg_url = Option()
        reg_url.get_by_name("registry_url")
        glow.registry_info["local"]["url"] = reg_url.value
        if not glow.registry_info["local"]["url"]:
            logging.error("No registry url found on Cver")
            return False

        reg_user = Option()
        reg_user.get_by_name("registry_user")
        glow.registry_info["local"]["user"] = reg_user.value
        if not glow.registry_info["local"]["user"]:
            logging.error("No registry user found on Cver")
            return False

        reg_pass = Option()
        reg_pass.get_by_name("registry_password")
        glow.registry_info["local"]["pass"] = reg_pass.value
        if not glow.registry_info["local"]["pass"]:
            logging.error("No registry password found on Cver")
            return False

        repository_general = Option()
        repository_general.get_by_name("repository_general")
        glow.registry_info["repository_general"] = repository_general.value
        if not glow.registry_info["repository_general"]:
            logging.error("No repository_general limit password found on Cver")
            return False

        # Get engine options

        cluster_presence_hours = Option()
        cluster_presence_hours.get_by_name("cluster_presence_hours")
        glow.engine_info["cluster_presence_hours"] = cluster_presence_hours.value
        if not glow.engine_info["cluster_presence_hours"]:
            logging.error("No cluster_presence_hours found.")
            return False

        engine_download_limit = Option()
        engine_download_limit.get_by_name("engine_download_limit")
        glow.engine_info["download_limit"] = engine_download_limit.value
        if not glow.engine_info["download_limit"]:
            logging.error("No download limit password found on Cver")
            return False

        download_process_limit = Option()
        download_process_limit.get_by_name("engine_download_process_limit")
        glow.engine_info["download_process_limit"] = download_process_limit.value
        if not glow.engine_info["download_process_limit"]:
            logging.error("No scan limit password found on Cver")
            return False

        download_process_limit = Option()
        download_process_limit.get_by_name("engine_scan_process_limit")
        glow.engine_info["scan_process_limit"] = download_process_limit.value
        if not glow.engine_info["download_process_limit"]:
            logging.error("No scan limit password found on Cver")
            return False

        engine_scan_limit = Option()
        engine_scan_limit.get_by_name("engine_scan_limit")
        glow.engine_info["scan_limit"] = engine_scan_limit.value
        if not glow.engine_info["scan_limit"]:
            logging.error("No scan limit found on Cver")
            return False

        engine_scan_fail_threshold = Option()
        engine_scan_fail_threshold.get_by_name("engine_scan_fail_threshold")
        glow.engine_info["scan_fail_threshold"] = engine_scan_limit.value
        if not glow.engine_info["scan_fail_threshold"]:
            logging.error("No scan engine threshold limit found.")
            return False

        # Log in to the local registry
        docker.registry_login(
            glow.registry_info["local"]["url"],
            glow.registry_info["local"]["user"],
            glow.registry_info["local"]["pass"])

        return True

<<<<<<< HEAD
    def run_cluster_presence(self) -> bool:
        self.presence_report = ClusterPresence().run()
        if not self.presence_report:
            logging.error("Failed to run cluster image presence")
            return False
        return True

    def create_priority(self, the_phase: str):
        self.engine_priorty = EnginePriority().run(phase=the_phase)
=======
    def run_cluster_presence(self):
        self.presence_report = ClusterPresence().run()
>>>>>>> origin/stage

    def run_downloads(self):
        """Engine Download runner. Here we'll download images waiting to be pulled down."""
        self.download_report = EngineDownload().run()

    def run_scans(self):
        logging.info("Running Engine Scan")
        self.scan_report = EngineScan().run()

    def run_cleanup(self):
        docker_images = docker.get_all_images()
        if not docker_images:
            return True
        for image in docker_images:
            docker.delete_image(image)
        return True

    def _get_registries(self) -> bool:
        """Get all registries we currently know about and store them in glow."""
        registries = Registries().get()
        for reg in registries:
            glow.registry_info["registries"][reg.id] = reg
        return True

    def _draw_download_report(self) -> str:
        """Log out the relevant info from the Engine Download report."""
        if not self.download_report:
            return ""

        msg = "Engine Download"
        msg += "\n\tDownloaded: %s/%s" % (
            self.download_report["downloaded"],
            self.download_report["download_limit"]
        )
        msg += "\n\tProcessed: %s" % self.download_report["proccessed_ibws"]
        if self.download_report["downloaded_images_success"]:
            msg += "\n\tSucessfull Downloads\n"
            for dl_success in self.download_report["downloaded_images_success"]:
                msg += "\t\t%s\n" % dl_success

        if len(self.download_report["downloaded_images_failed"]) > 0:
            msg += "\n\tFailed Downloads\n"
            for dl_fail in self.download_report["downloaded_images_failed"]:
                msg += "\t\t%s\n" % dl_fail

        return msg

    def _draw_scan_report(self) -> str:
        """Log out the relevant info from the Engine Download report."""
        print(self.scan_report)
        if not self.scan_report:
            return ""
        msg = "Engine Scan"
        msg += "\n\tScanned: %s/%s" % (
            self.scan_report["scanned"],
            self.scan_report["scan_limit"]
        )
        msg += "\n\tProcessed: %s\n" % self.scan_report["proccessed_ibws"]
        if self.scan_report["scanned_images_success"]:
            msg += "\tSuccessful Scans\n"
            for image in self.scan_report["scanned_images_success"]:
                msg += "\t\t%s\n" % image

        if self.scan_report["scanned_images_failed"]:
            msg += "\tFailed Scans\n"
            for image in self.scan_report["scanned_images_failed"]:
                msg += "\t\t%s\n" % image
        msg += "\n"
        return msg


def parse_args():
    """Parse CLI args"""
    parser = argparse.ArgumentParser(description="Cver Engine")
    parser.add_argument(
        "action",
        nargs='?',
        default="all",
        help="Action to run: download,scan default: all")
    the_args = parser.parse_args()
    return the_args


if __name__ == "__main__":
    args = parse_args()
    Engine(args).run()


# End File: cver/src/cver/engine/engine.py
