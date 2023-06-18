"""
    Cver Migrate
    Data - Misc
    Create the misc data needed for an installation of Cver Api.

"""
import logging

from cver.api.models.scanner import Scanner


class DataMisc:

    def create(self) -> bool:
        """Create the misc data needed for an installation of Cver Api."""
        self.create_scanner()

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