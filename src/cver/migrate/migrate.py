"""
    Cver Migrate

"""
import logging
from logging.config import dictConfig
import os
import subprocess

from cver.api.utils import db
from cver.api.utils import glow
from cver.api.models.migration import Migration
from cver.migrate.data.data_rbac import DataRbac
from cver.migrate.data.data_users import DataUsers
from cver.migrate.data.data_misc import DataMisc


CURRENT_MIGRATION = 2

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


class Migrate:

    def __init__(self):
        self.role_admin_id = None

    def run(self):
        """Primary entry point for migrations."""
        logging.info("Working with database %s" % glow.db["NAME"])
        self.create_database()
        db.connect()
        self.last_migration = self.get_migration_info()
        self.this_migration = Migration()
        self.run_migrations()
        self.create_rbac()
        self.create_users()
        self.create_misc()
        logging.info("Migrations were successful")
        # self.create_table_sql()

    def create_database(self) -> True:
        """Create the database for CVER.
        @todo: This could be done more securily by attempting to connect to the database first.
        """
        conn, cursor = db.connect_no_db(glow.db)
        sql = "CREATE DATABASE  IF NOT EXISTS `%s`;" % glow.db["NAME"]
        cursor.execute(sql)
        conn.commit()
        logging.info("Created database: %s" % glow.db["NAME"])
        return True

    def get_migration_info(self) -> Migration:
        """Get the info from the last migration ran"""
        Migration().create_table()
        last = Migration()
        last.get_last_successful()
        if not last.id:
            return False
        return last

    def run_migrations(self) -> bool:
        """Determine the migrations we need to run, and execute them."""
        if self.last_migration:
            logging.info("Last migration ran: #%s" % self.last_migration.number)
        else:
            logging.info("Running first migration")
        if self.last_migration and CURRENT_MIGRATION == self.last_migration.number:
            logging.info("Migration: %s Caught Up" % CURRENT_MIGRATION)
            return True
        if self.last_migration:
            migration_no = self.last_migration.number + 1
        else:
            migration_no = 1

        while migration_no <= CURRENT_MIGRATION:
            self.run_migration(migration_no)
            migration_no += 1

        return True

    def run_migration(self, migration_no: int):
        """Running a single migration."""
        logging.info("Running Migration #%s" % migration_no)
        m = Migration()
        m.number = migration_no
        migration_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "sql/up/%s.sql" % migration_no)
        cmd = "mysql -h %s --port %s -u %s --password=%s %s < %s" % (
            glow.db["HOST"],
            glow.db["PORT"],
            glow.db["USER"],
            glow.db["PASS"],
            glow.db["NAME"],
            migration_file
        )
        if not os.path.exists(migration_file):
            logging.critical("File doesnt exist")
            return False

        try:
            child = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            rc = child.returncode
            db.connect()
            # If the command exits higher than 0 save that.
            if rc and rc > 0:
                logging.critical("Failed to run migration: %s")
                m.success = False
                m.save()
                return False
            m.success = True
            m.save()
            return True
        except Exception as e:
            logging.critical("Failed to run migration: %s" % e)
            m.success = False
            m.save()
            exit(1)

    def create_rbac(self):
        """Create the Rbac roles/role perms and perms."""
        logging.info("Creating Roles")
        self.rbac = DataRbac().create()

    def create_users(self):
        """Create the users and api keys."""
        logging.info("Creating Users and Keys")
        DataUsers().create(self.rbac)

    def create_misc(self):
        """Create misc data."""
        logging.info("Creating misc data")
        DataMisc().create()

    # def create_table_sql(self):
    #     """Create table SQL for migrations."""
    #     print(ScanRaw().create_table_sql())


if __name__ == "__main__":
    Migrate().run()


# End File: cver/src/migrate/migrate.py
