"""
    Cver Migrate
    Data - Rbac

"""
from datetime import datetime
import logging
import os

import arrow

from cver.api.utils import glow
from cver.api.collects.roles import Roles
from cver.api.models.api_key import ApiKey
from cver.api.models.user import User
from cver.api.models.organization import Organization
from cver.api.utils import auth


class DataUsers:

    def __init__(self):
        self.org_id = 1
        self.roles = {}
        self.get_all_roles()

    def get_all_roles(self):
        roles = Roles().get_all()
        self.roles = {}
        for role in roles:
            self.roles[role.slug_name] = role
        return True

    def create(self) -> bool:
        """Create the first user, and test users if this is a test environment."""
        self.create_first_org()
        if not glow.general["CVER_TEST"]:
            logging.info("")
            self.create_first_admin()
        else:
            self.create_first_test_user()
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

    def create_first_admin(self) -> bool:
        """Create the first admin level user, but only if one doesn't already exist."""
        logging.info("Creating First Admin User")
        client_id = auth.generate_client_id()
        api_key = auth.generate_api_key()
        expire_at = (arrow.utcnow().shift(hours=4)).datetime
        self.create_user(
            "admin",
            "admin@example.com",
            self.roles["admin"].id,
            client_id,
            api_key,
            expire_at)
        return True

    def create_first_test_user(self) -> bool:
        """Create the first admin level user for a test environment, but only if one doesn't
        already exist.
        """
        logging.info("Creating First Admin User")
        client_id = os.environ.get("CVER_TEST_ADMIN_CLIENT_ID")
        api_key = os.environ.get("CVER_TEST_ADMIN_API_KEY")
        self.create_user("admin", "admin@example.com", self.roles["admin"].id, client_id, api_key)
        return True

    def create_test_users(self) -> bool:
        """Create the test users for Ingestion and Engine."""
        if not glow.general["CVER_TEST"]:
            logging.info("Not creating test users")
            return True

        logging.info("Creating Test Users")
        client_id = os.environ.get("CVER_TEST_INGEST_CLIENT_ID")
        if not client_id:
            logging.warning("Missing CVER_TEST_INGEST_CLIENT_ID env var, skipping user creation.")
            return False
        api_key = os.environ.get("CVER_TEST_INGEST_API_KEY")
        roles_id = self.roles["ingestor"].id
        self.create_user("test-ingest", "ingest@example.com", roles_id, client_id, api_key)

        # Create User: test-engine
        client_id = os.environ.get("CVER_TEST_ENGINE_CLIENT_ID")
        if not client_id:
            logging.warning("Missing CVER_TEST_ENGINE_CLIENT_ID env var, skipping user creation.")
            return False
        api_key = os.environ.get("CVER_TEST_ENGINE_API_KEY")
        roles_id = self.roles["engineer"].id
        self.create_user("test-engine", "engine@example.com", roles_id, client_id, api_key)

    def create_user(
            self,
            user_name: str,
            user_email: str,
            role_id: int,
            client_id: str,
            api_key_str: str,
            expiration_date: datetime = None
    ) -> bool:
        user = User()
        if user.get_by_email(user_email):
            logging.info("Not Creating user arelady exists: %s" % user)
            return False
        if user.get_by_name(user_name):
            logging.info("Not Creating user arelady exists: %s" % user)
            return False

        if not role_id:
            logging.error("User is missing Role.id, cannot create.")
            return True

        user.name = user_name
        user.role_id = role_id
        user.org_id = self.org_id
        if not user.save():
            logging.error("Couldnt save %s" % user)
            return False
        api_key = ApiKey()
        api_key.user_id = user.id
        api_key.client_id = client_id
        if expiration_date:
            api_key.expiration_date = expiration_date
        if api_key.get_by_field(field="client_id", value=client_id):
            msg = "Not creating ApiKey client_id for user: %s, client id: %s already exists" % (
                user,
                client_id
            )
            logging.info(msg)
            return False

        api_key.key = auth.generate_hash(api_key_str)
        api_key.save()
        print("Created")
        print("\t%s" % user)
        print("\tClient ID: %s" % client_id)
        print("\tApi Key: %s" % api_key_str)
        if expiration_date:
            print("\tKey will expire in 4 hours!")
        return True

# End File: cver/src/migrate/data/data_rbac.py
