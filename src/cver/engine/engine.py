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
from cver.cver_client.models.option import Option
from cver.engine.modules.engine_download import EngineDownload
from cver.engine.modules.engine_scan import EngineScan

logging.config.dictConfig(log_config)
logger = logging.getLogger(__name__)
logger.propagate = True


class Engine:
    def __init__(self):
        self.registry_url = None
        self.registry_user = None
        self.registry_password = None
        self.download_limit = 1
        self.downloaded = 0
        self.scan_limit = 1
        self.scanned = 0

    def run(self):
        if not self.preflight():
            logging.critical("Pre flight checks failed.")
            exit(1)
        self.run_downloads()
        self.run_scans()

    def preflight(self):
        """Check that have a registry to push/pull to/from."""
        reg_url = Option()
        reg_url.get_by_name("registry_url")
        self.registry_url = reg_url.value
        if not self.registry_url:
            logging.error("No registry url found on Cver")
            return False

        reg_user = Option()
        reg_user.get_by_name("registry_user")
        self.registry_user = reg_user.value
        if not self.registry_user:
            logging.error("No registry user found on Cver")
            return False

        reg_pass = Option()
        reg_pass.get_by_name("registry_password")
        self.registry_password = reg_pass.value
        if not self.registry_password:
            logging.error("No registry password found on Cver")
            return False

        reg_pull_thru_docker = Option()
        reg_pull_thru_docker.get_by_name("registry_pull_thru_docker_io")
        self.registry_pull_thru_docker_io = reg_pull_thru_docker.value
        if not self.registry_pull_thru_docker_io:
            logging.error("No registry pull through found on Cver")
            return False

        docker.registry_login(self.registry_url, self.registry_user, self.registry_password)
        return True

    def run_downloads(self):
        """Engine Download runner. Here we'll download images waiting to be pulled down."""
        EngineDownload().run()

    def run_scans(self):
        logging.info("Running Engine Scan")
        EngineScan().run()


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
