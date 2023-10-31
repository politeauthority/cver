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
from cver.cver_client.collections.image_builds import ImageBuilds
from cver.cver_client.models.option import Option
from cver.engine.modules.engine_download import EngineDownload
from cver.engine.modules.engine_scan import EngineScan
from cver.engine.utils import glow

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Engine:

    def __init__(self):
        self.download_report = {}
        self.scan_report = {}

    def run(self):
        logging.info("Starting Cver Engine")
        if not self.preflight():
            logging.critical("Pre flight checks failed.")
            exit(1)
        self.run_setup()
        self.run_downloads()
        self.run_scans()
        logging.info("Engine Process Complete")
        msg = "\n\nEngine\n"
        self._draw_download_report()
        self._draw_scan_report()
        logging.info(msg)

    def preflight(self):
        """Check that have a registry to push/pull to/from."""
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

        # Get engine options
        engine_download_limit = Option()
        engine_download_limit.get_by_name("engine_download_limit")
        glow.engine_info["download_limit"] = engine_download_limit.value
        if not glow.engine_info["download_limit"]:
            logging.error("No download limit password found on Cver")
            return False

        engine_scan_limit = Option()
        engine_scan_limit.get_by_name("engine_scan_limit")
        glow.engine_info["scan_limit"] = engine_scan_limit.value
        if not glow.engine_info["scan_limit"]:
            logging.error("No scan limit password found on Cver")
            return False

        docker.registry_login(
            glow.registry_info["local"]["url"],
            glow.registry_info["local"]["user"],
            glow.registry_info["local"]["pass"])

        return True

    def run_setup(self):
        self._setup_download()

    def run_downloads(self):
        """Engine Download runner. Here we'll download images waiting to be pulled down."""
        self.download_report = EngineDownload().run()

    def run_scans(self):
        logging.info("Running Engine Scan")
        self.scan_report = EngineScan().run()

    def _setup_download(self):
        ib_col = ImageBuilds()
        args = {
            "feilds": {
                "sync_enabled": {
                    "value": True
                }
            },
            "order_by": {
                "field": "sync_last_ts",
                "direction": "DESC"
            },
            "limit": glow.engine_info["download_limit"]
        }
        ibs = ib_col.get(args)
        print(ibs)

    def _draw_download_report(self) -> bool:
        """Log out the relevant info from the Engine Download report."""
        if "downloaded" not in self.download_report:
            return True
        msg = "\tDownloaded: %s/%s" % (
            self.download_report["downloaded"],
            self.download_report["download_limit"]
        )
        logging.info(msg)
        return True

    def _draw_scan_report(self) -> bool:
        """Log out the relevant info from the Engine Download report."""
        print(self.scan_report)
        # if not self.scan_report:
        #     return True
        # msg = "\nScanned: %s/%s" % (
        #     self.scan_report["downloaded"],
        #     self.scan_report["download_limit"]
        # )
        # logging.info(msg)
        return True


def parse_args(args):
    """Parse CLI args"""
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('-c', '--count')      # option that takes a value
    parser.add_argument('-v', '--verbose', action='store_true')  # on/off flag
    print(args)
    return parser


if __name__ == "__main__":
    Engine().run()


# End File: cver/src/cver/engine/engine.py
