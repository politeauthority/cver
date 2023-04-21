"""
"""
from cver.api.utils import db
from cver.api.utils import glow
from cver.api.utils import glow

from cver.api.models.cve import Cve
from cver.api.models.cvss import Cvss
from cver.api.models.entity_meta import EntityMeta
from cver.api.models.option import Option
from cver.api.models.software import Software
from cver.api.models.user import User


def run():
    # Cve().create_table()
    # Cvss().create_table()
    EntityMeta().create_table()
    Option().create_table()
    # Product().create_table()
    Software().create_table()
    User().create_table()
    # Vendor().create_table()


if __name__ == "__main__":
    glow.db = db.connect()
    run()


# End File: cver/src/migrate/migrate.py
