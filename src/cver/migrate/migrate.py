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
from cver.api.models.software import Software

from cver.api.collects.users import Users
from cver.api.models.api_key import ApiKey
from cver.api.models.user import User
from cver.api.utils import auth


CURRENT_MIGRATION = 1
db.connect()

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

    def run(self):
        """Primary entry point for migrations."""
        logging.info("Working with database %s" % glow.db["NAME"])
        self.last_migration = self.get_migration_info()
        self.this_migration = Migration()
        self.run_migrations()
        self.create_first_user()
        # self.create_data()

    def get_migration_info(self) -> Migration:
        """Get the info from the last migration ran"""
        Migration().create_table()
        last = Migration()
        last.get_last()
        if not last.id:
            return False
        return last

    def run_migrations(self) -> bool:
        """Run the SQL migrations needed to get the database up to speed."""
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
            logging.error("File doesnt exist")
            exit(1)
        try:
            subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
            db.connect()
            m.success = True
            m.save()
            return True
        except Exception as e:
            logging.error("Failed to run migration: %s" % e)
            m.success = False
            m.save()
            exit(1)

    def create_first_user(self):
        """Create the first admin level user, but only if one doesn't already exist."""
        logging.info("Creating first user")
        if glow.general["CVER_ENV"] == "test":
            self.make_test_user()
            return True
        admin_users = Users().get_admins()
        if admin_users:
            logging.info("Not creating an admin, %s already exist" % len(admin_users))
            return True
    
        user = User()
        user.email = "admin@example.com"
        user.name = "admin"
        user.role_id = 1
        user.save()
        print("Created: %s" % user)
        client_id = auth.generate_client_id()
        key = auth.generate_api_key()
        api_key = ApiKey()
        api_key.user_id = user.id
        api_key.client_id = client_id
        api_key.key = auth.generate_hash(key)

        api_key.save()
        print("Created")
        print("\t%s" % user)
        print("\t%s" % api_key)
        print("\t Client ID: %s" % client_id)
        print("\t Api Key: %s" % key)

    def make_test_user(self):
        user = User()
        if user.get_by_email("test@example.com"):
            logging.info("Test user already exists: %s" % user)
            return False
        user.email = "test@example.com"

    def create_data(self):
        """Create already tracked apps."""
        logging.info("Creating Software")
        softwares = ["emby"]
        sotfware = Software()

        for a_software_name in softwares:
            software = Software()
            if not software.get_by_name(a_software_name):
                sotfware.name = a_software_name
                sotfware.slug_name = a_software_name
                sotfware.save()
            logging.info("Wrote app %s" % a_software_name)
        return


if __name__ == "__main__":
    Migrate().run()


# End File: cver/src/migrate/migrate.py
