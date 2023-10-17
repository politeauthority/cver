"""
    Examples - Cver Client
    Setup Instance
    Basic setup and administration script for the CverApi
    Using the CverClient, we'll set up our Docker registry details.

"""
import logging

from cver.cver_client.models.cluster import Cluster
from cver.cver_client.models.option import Option

REGISTRY_URL = "harbor.squid-ink.us"
REGISTRY_USER = "politeauthority"
REGISTRY_PASSWORD = "bSX6gJTcUKnGbXYLd9nhMSvRo"
ORG_ID = 1


class SetupCver:

    def __init__(self):
        self.org_id = ORG_ID
        self.successes = 0
        self.failures = 0

    def run(self):
        self.create_cluster()
        self.options_registry()
        self.create_user()

    def create_cluster(self):
        """Create the first cluster"""
        cluster = Cluster()
        cluster.name = "Colfax K8s"
        if cluster.get_by_name():
            logging.info("Cluster has already been created: %s" % cluster)
            return True
        cluster.org_id = self.org_id

        if cluster.save():
            self.successes += 1
            logging.info("Successfully created Cluster")
        else:
            self.failures += 1
            logging.error("Failed to make Cluster")

    def options_registry(self):
        """Update registry options."""
        opt_reg = Option()
        opt_reg.get_by_name("registry_url")
        opt_reg.value = REGISTRY_URL
        if opt_reg.save():
            logging.info("Saved registry_url")
        else:
            self.failures += 1
            logging.error("Failed to make Cluster")

        opt_reg = Option()
        opt_reg.get_by_name("registry_user")
        opt_reg.value = REGISTRY_USER
        if opt_reg.save():
            self.successes += 1
            logging.error("Saved registry_usr")
        else:
            self.failures += 1
            logging.error("Failed registry_usr")

        opt_reg = Option()
        opt_reg.get_by_name("registry_password")
        opt_reg.value = REGISTRY_PASSWORD
        if opt_reg.save():
            self.successes += 1
            logging.info("Saved registry_password")
        else:
            self.failures += 1
            logging.error("Saved registry_password")

        opt_reg = Option()
        opt_reg.get_by_name("registry_pull_thru_docker_io")
        opt_reg.value = "cver-docker-hub"
        if opt_reg.save():
            self.successes += 1
            logging.info("Saved registry_pull_thru_docker_io")
        else:
            self.failures += 1
            logging.error("Failed registry_pull_thru_docker_io")

        # opt_reg = Option()
        # opt_reg.get_by_name("registry_pull_thru_quay_io")
        # opt_reg.value = "cver-quay"
        # if opt_reg.save():
        #     self.successes += 1
        #     logging.info("Saved registry_pull_thru_quay_io")
        # else:
        #     self.failures += 1
        #     logging.error("Failed registry_pull_thru_quay_io")

    def create_user(self):
        logging.info("Create User")


if __name__ == "__main__":
    SetupCver().run()

# End File: cver/examples/cver-client/setup_instance.py
