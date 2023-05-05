"""
    Cver Migrate

"""
import os

from cver.api.utils import db
from cver.api.utils import glow
from cver.shared.utils import log

from cver.api.models.entity_meta import EntityMeta
from cver.api.models.image import Image
from cver.api.models.image_build import ImageBuild
from cver.api.models.migration import Migration
from cver.api.models.option import Option
from cver.api.models.scan import Scan
from cver.api.models.scanner import Scanner
from cver.api.models.software import Software
from cver.api.models.user import User


CVER_DB_NAME = os.environ.get("CVER_DB_NAME")
CURRENT_MIGRATION = 1


class Migrate:

    def run(self):
        log.info("Working with database %s" % CVER_DB_NAME)
        self.last_migration = self.get_migration_info()
        self.this_migration = Migration()
        self.run_migrations()
        self.create_data()

    def get_migration_info(self):
        """Get the info from the last migration ran"""
        Migration().create_table()
        last = Migration()
        last.get_last()
        if not last.id:
            return False
        return last

    def run_migrations(self):
        if not self.last_migration:
            print("First run of migrations.")
            self.create_initial_tables()
            self.this_migration.number = 1
            self.this_migration.success = True
            self.this_migration.save()
            log.info("Migration %s Succeeded" % self.this_migration.number)
            return True
        elif CURRENT_MIGRATION == self.last_migration.number:
            log.info("Migration: %s Caught Up" % CURRENT_MIGRATION)
            return True
        else:
            log.warning("Not sure what to do here")

    def create_initial_tables(self):
        """Create tables."""
        log.info("Creating tables")
        EntityMeta().create_table()
        Image().create_table()
        ImageBuild().create_table()
        Option().create_table()
        Scan().create_table()
        Scanner().create_table()
        Software().create_table()
        Software().create_table()
        User().create_table()

    def create_data(self):
        """Create already tracked apps."""
        log.info("Creating Software")
        softwares = ["emby"]
        sotfware = Software()

        for a_software_name in softwares:
            software = Software()
            if not software.get_by_name(a_software_name):
                sotfware.name = a_software_name
                sotfware.slug_name = a_software_name
                sotfware.save()
            log.info("Wrote app %s" % a_software_name)
        return


if __name__ == "__main__":
    glow.db = db.connect()
    Migrate().run()


# End File: cver/src/migrate/migrate.py
