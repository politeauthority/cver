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
        self._make_option("registry_url")
        self._make_option("registry_user")
        self._make_option("registry_password")
        self._make_option("registry_pull_thru_docker_io")
        self._make_option("repository_general")
        logging.info("Registry options create successful")
        return True

    def create_engine_options(self):
        """Create scan and limit option details."""
        self._make_option("engine_download_limit", 1)
        self._make_option("engine_download_process_limit", 1)
        self._make_option("engine_scan_limit", 1)
        self._make_option("engine_scan_process_limit", 1)
        logging.info("Engine options create successful")
        return True

    def _make_option(self, option_name, option_value=None) -> bool:
        opt = Option()
        opt.name = option_name
        if not opt.get_by_name():
            opt.type = "int"
            opt.acl_write = ["write-all"]
            opt.acl_read = ["read-all"]
            if option_value:
                opt.value = option_value
            if not opt.save():
                logging.error("Could not create option: %s" % option_name)
                return False
        return True


# End File: cver/src/migrate/data/data_options.py
