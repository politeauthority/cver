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
        self.create_engine_options()

    def create_registry_options(self):
        """Create container registry details."""
        # Registry URL
        registry_url = Option()
        registry_url.name = "registry_url"
        if not registry_url.get_by_name():
            registry_url.type = "str"
            registry_url.acl_write = ["write-all"]
            registry_url.acl_read = ["read-all"]
            registry_url.save()

        # Registry User
        registry_user = Option()
        registry_user.name = "registry_user"
        if not registry_user.get_by_name():
            registry_user.type = "str"
            registry_user.acl_write = ["write-all"]
            registry_user.acl_read = ["read-all"]
            registry_user.save()

        # Registry Password
        registry_password = Option()
        registry_password.name = "registry_password"
        if not registry_password.get_by_name():
            registry_password.type = "str"
            registry_password.acl_write = ["write-all"]
            registry_password.acl_read = ["read-all"]
            registry_password.hide_value = True
            registry_password.save()

        # Registry Docker Hub Pull Through
        registry_pull_through = Option()
        registry_pull_through.name = "registry_pull_thru_docker_io"
        if not registry_pull_through.get_by_name():
            registry_pull_through.type = "str"
            registry_pull_through.acl_write = ["write-all"]
            registry_pull_through.acl_read = ["read-all"]
            registry_pull_through.save()

        # Repository General
        registry_pull_through = Option()
        registry_pull_through.name = "repository_general"
        if not registry_pull_through.get_by_name():
            registry_pull_through.type = "str"
            registry_pull_through.acl_write = ["write-all"]
            registry_pull_through.acl_read = ["read-all"]
            registry_pull_through.save()

        logging.info("Registry options create successful")

    def create_engine_options(self):
        """Create scan and limit option details."""
        # Registry URL
        opt = Option()
        opt.name = "engine_download_limit"
        if not opt.get_by_name():
            opt.type = "int"
            opt.acl_write = ["write-all"]
            opt.acl_read = ["read-all"]
            opt.value = 1
            opt.save()
        opt = Option()
        opt.name = "engine_scan_limit"
        if not opt.get_by_name():
            opt.type = "int"
            opt.acl_write = ["write-all"]
            opt.acl_read = ["read-all"]
            opt.value = 1
            opt.save()
        logging.info("Engine options create successful")

# End File: cver/src/migrate/data/data_options.py
