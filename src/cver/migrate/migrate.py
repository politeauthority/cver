"""
    Cver Migrate

"""
from cver.api.utils import db
from cver.api.utils import glow
from cver.shared.utils import log

from cver.api.models.entity_meta import EntityMeta
from cver.api.models.image import Image
from cver.api.models.image_build import ImageBuild
from cver.api.models.option import Option
from cver.api.models.scan import Scan
from cver.api.models.scanner import Scanner
from cver.api.models.software import Software
from cver.api.models.user import User


class Migrate:

    def run(self):
        self.create_table()
        self.create_apps()

    def create_table(self):
        """Create tables.
        """
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

    def create_apps(self):
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
