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
from cver.api.models.role import Role
from cver.api.models.role_perm import RolePerm
from cver.api.models.perm import Perm

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
        self.create_roles()
        self.create_users()
        # self.create_data()

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

    def create_roles(self):
        """Create the Rbac roles/role perms and perms."""
        logging.info("Creating Roles")
        self.create_role_admin()

    def create_role_admin(self):
        """Create the admin role with read/write all."""
        logging.info("Creating Admin Role")
        role = Role()
        role.name = "Admin"
        role.slug_name = "admin"
        role.save()
        self.role_admin_id = role.id

        perm = Perm()
        perm.name = "Read All"
        perm.slug_name = "read-all"
        perm.save()
        perm_read_all_id = perm.id

        perm = Perm()
        perm.name = "Read All"
        perm.slug_name = "read-all"
        perm.save()
        perm_read_all_id = perm.id

        perm = Perm()
        perm.name = "Write All"
        perm.slug_name = "write-all"
        perm.save()
        perm_read_all_id = perm.id

        role_perm = RolePerm()
        role_perm.role_id = self.role_admin_id
        role_perm.perm_id = perm_read_all_id
        role_perm.save()

    def create_users(self):
        """Create the users and api keys."""
        self.create_first_user()
        self.create_test_user()

    def create_first_user(self):
        """Create the first admin level user, but only if one doesn't already exist."""
        logging.info("Checking need for user creation")
        admin_users = Users().get_admins()
        if admin_users:
            logging.info("Not creating an admin, %s already exist" % len(admin_users))
            return True

        user = User()
        user.email = "admin@example.com"
        user.name = "admin"
        user.role_id = self.role_admin_id
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

    def create_test_user(self):
        """Create test Users, with given pre-known keys."""
        if not glow.general["CVER_TEST"]:
            logging.info("Not creating test users")
            return False

        user = User()
        if user.get_by_email("test@example.com"):
            logging.info("Test user already exists: %s" % user)
            return False
        test_client_id = os.environ.get("CVER_TEST_CLIENT_ID")
        if not test_client_id:
            logging.error("Missing: CVER_TEST_CLIENT_ID")
            return False
        test_api_key = os.environ.get("CVER_TEST_API_KEY")
        if not test_api_key:
            logging.error("Missing: CVER_TEST_API_KEY")
            return False

        user = User()
        user.email = "test@example.com"
        user.name = "test"
        user.role_id = self.role_admin_id
        user.save()
        client_id = test_client_id
        api_key = ApiKey()
        api_key.user_id = user.id
        api_key.client_id = client_id
        api_key.key = auth.generate_hash(test_api_key)
        api_key.save()
        print("Created")
        print("\t%s" % user)
        print("\t%s" % api_key)
        print("\t Client ID: %s" % client_id)
        print("\t Api Key: %s" % test_api_key)

        return True

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
