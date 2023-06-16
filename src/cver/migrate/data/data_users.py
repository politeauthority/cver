"""
    Cver Migrate
    Data - Rbac

"""
import logging
import os

from cver.api.utils import glow
from cver.api.collects.users import Users
from cver.api.models.api_key import ApiKey
from cver.api.models.user import User
from cver.api.utils import auth


class DataUsers:

    def __init__(self):
        self.rbac = None

    def create(self, rbac: dict) -> bool:
        """Create the first user, and test users if this is a test environment."""
        self.rbac = rbac
        self.role_admin_id = rbac["admin_role_id"]
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
        print("\t Client ID: %s" % client_id)
        print("\t Api Key: %s" % test_api_key)

        return True


# End File: cver/src/migrate/data/data_rbac.py
