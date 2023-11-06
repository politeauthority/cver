"""
    Cver Migrate
    Data - Rbac

"""
import logging
import os

from cver.api.utils import glow
from cver.api.collects.users import Users
from cver.api.collects.roles import Roles
from cver.api.models.api_key import ApiKey
from cver.api.models.user import User
from cver.api.models.organization import Organization
from cver.api.utils import auth


class DataUsers:

    def __init__(self):
        self.rbac = None
        self.org_id = None
        self.roles = {}
        self.get_all_roles()

    def get_all_roles(self):
        roles = Roles().get_all()
        self.roles = {}
        for role in roles:
            self.roles[role.slug_name] = role
        return True

    def create(self, rbac: dict) -> bool:
        """Create the first user, and test users if this is a test environment."""
        self.rbac = rbac
        self.role_admin_id = rbac["admin_role_id"]
        self.create_first_org()
        self.create_first_user()
        self.create_test_users()

    def create_first_org(self) -> bool:
        """Create the first Organization
        @todo: Make this more dynamic.
        """
        org = Organization()
        if org.get_by_email("test@example.com"):
            logging.info("Organization %s already exists, skipping creation" % org.name)
            self.org_id = org.id
            return True
        org.name = "First Org"
        org.email = "test@example.com"
        org.save()
        logging.info("Created Org: %s" % org)
        self.org_id = org.id
        return True

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
        user.org_id = self.org_id
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
        print("\t Client ID: %s" % client_id)
        print("\t Api Key: %s" % key)

    def create_test_users(self):
        if not glow.general["CVER_TEST"]:
            logging.info("Not creating test users")
            return True

        # Create User: test-admin
        client_id = os.environ.get("CVER_TEST_CLIENT_ID")
        api_key = os.environ.get("CVER_TEST_ADMIN_API_KEY")
        roles_id = self.roles["admin"].id
        self.create_user("test-admin", "test-admin@example.com", roles_id, client_id, api_key)

        # Create User: test-ingest
        client_id = os.environ.get("CVER_TEST_INGEST_CLIENT_ID")
        api_key = os.environ.get("CVER_TEST_INGEST_API_KEY")
        roles_id = self.roles["ingestor"].id
        self.create_user("test-ingest", "ingest@example.com", roles_id, client_id, api_key)

        # # Create User: test-engine
        # client_id = os.environ.get("CVER_TEST_ENGINE_CLIENT_ID")
        # api_key = os.environ.get("CVER_TEST_ENGINE_API_KEY")
        # roles_id = self.roles["engine"].id
        # self.create_user("test-engine", "engine@example.com", roles_id, client_id, api_key)

    def create_user(self, user_name, user_email, role_id, client_id, api_key) -> bool:
        user = User()
        user.get_by_email(user_email)
        if user:
            logging.debug("Not Creating user arelady exists: %s" % user)
            return False
        user.name = user_name
        user.role_id = role_id
        user.org_id = 1
        if not user.save():
            logging.error("Couldnt save %s" % user)
            return False
        api_key = ApiKey()
        api_key.user_id = user.id
        api_key.client_id = client_id
        api_key.key = auth.generate_hash(api_key)
        api_key.save()
        print("Created")
        print("\t%s" % user)
        print("\t Client ID: %s" % client_id)
        print("\t Api Key: %s" % api_key)
        return True

# End File: cver/src/migrate/data/data_rbac.py
