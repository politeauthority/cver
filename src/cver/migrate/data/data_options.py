"""
    Cver Migrate
    Data - Options

"""
import logging

from cver.api.models.option import Option


class DataOptions:

    def create(self) -> bool:
        """Create the Options."""
        self.create_registry_options()

    def create_registry_options(self):
        """Create container registry details."""
        # Registry URL
        registry_url = Option()
        registry_url.type = "str"
        registry_url.name = "registry_url"
        registry_url.acl_write = ["write-all"]
        registry_url.acl_read = ["read-all"]
        registry_url.save()

        # Registry User
        registry_user = Option()
        registry_user.type = "str"
        registry_user.name = "registry_user"
        registry_user.acl_write = ["write-all"]
        registry_user.acl_read = ["read-all"]
        registry_user.save()

        # Registry Password
        registry_password = Option()
        registry_password.type = "str"
        registry_password.name = "registry_password"
        registry_password.acl_write = ["write-all"]
        registry_password.acl_read = ["read-all"]
        registry_password.hide_value = True
        registry_password.save()

        # Registry Docker Hub Pull Through
        registry_password = Option()
        registry_password.type = "str"
        registry_password.name = "registry_pull_thru_docker_io"
        registry_password.acl_write = ["write-all"]
        registry_password.acl_read = ["read-all"]
        registry_password.save()

        logging.info("Options create successful")

# End File: cver/src/migrate/data/data_options.py
