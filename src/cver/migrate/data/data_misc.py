"""
    Cver Migrate
    Data - Misc
    Create the misc data needed for an installation of Cver Api.

"""
import logging

from cver.api.models.cluster import Cluster
from cver.api.models.scanner import Scanner


class DataMisc:

    def create(self) -> bool:
        """Create the misc data needed for an installation of Cver Api."""
        self.create_cluster()
        self.create_scanner()

    def create_cluster(self) -> bool:
        """Create the first Cluster.
        @todo: We should probably not assume the org id is 1, should do that better.
        """
        cluster = Cluster()
        if cluster.get_by_name("default"):
            return True
        cluster.name = "default"
        cluster.org_id = 1
        cluster.save()
        logging.info("Created Cluster")
        return True

    def create_scanner(self) -> bool:
        """Create the first admin level user, but only if one doesn't already exist."""
        logging.info("Checking need for scanner creation")
        scanner = Scanner()
        if scanner.get_by_name("Trivy"):
            return True

        scanner.name = "Trivy"
        scanner.save()
        logging.info("Created: %s" % scanner)
        return True


# End File: cver/src/migrate/data/data_misc.py
