"""
    Cver Migrate
    Data - Options

"""
import logging
import os

from cver.api.models.option import Option
from cver.api.utils import glow


class DataOptions:

    def create(self) -> bool:
        """Create the Options."""
        self.create_registry_options()
        self.create_engine_options()
        self.create_registry_option_values()

    def create_registry_options(self):
        """Create container registry details."""
        self._make_option("registry_url", "str")
        self._make_option("registry_user", "Str")
        self._make_option("registry_password", "str")
        self._make_option("registry_pull_thru_docker_io", "str")
        self._make_option("repository_general", "str")
        logging.info("Registry options create successful")
        return True

    def create_engine_options(self):
        """Create engine download scan and limit option details."""
        self._make_option("engine_download_limit", "int", 1)
        self._make_option("engine_download_process_limit", "int", 1)
        self._make_option("engine_download_interval", "int", 168)
        self._make_option("engine_scan_limit", "int", 1)
        self._make_option("engine_scan_process_limit", "int", 1)
        self._make_option("engine_scan_interval", "int", 168)
        logging.info("Engine options create successful")
        return True

    def create_registry_option_values(self):
        """Create the option test values if we are in a test environment."""
        if not glow.general["CVER_TEST"]:
            return True
        logging.info("Setting test option values")
        opt_reg_url = Option()
        opt_reg_url.get_by_name("registry_url")
        opt_reg_url.type = "str"
        opt_reg_url.value = os.environ.get("CVER_TEST_OPT_REGISTRY_URL")
        opt_reg_url.save()

        opt_reg_user = Option()
        opt_reg_user.get_by_name("registry_user")
        opt_reg_user.type = "str"
        opt_reg_user.value = os.environ.get("CVER_TEST_OPT_REGISTRY_USER")
        opt_reg_user.save()

        opt_reg_pass = Option()
        opt_reg_pass.get_by_name("registry_password")
        opt_reg_pass.type = "str"
        opt_reg_pass.value = os.environ.get("CVER_TEST_OPT_REGISTRY_PASS")
        opt_reg_pass.save()

        opt_reg_repo_gen = Option()
        opt_reg_repo_gen.get_by_name("repository_general")
        opt_reg_repo_gen.type = "str"
        opt_reg_repo_gen.value = os.environ.get("CVER_TEST_OPT_REGISTRY_REPO_GEN")
        opt_reg_repo_gen.save()
        logging.info("Saved registry Option values")

    def _make_option(self, option_name, option_type: str, option_value=None, ) -> bool:
        opt = Option()
        opt.name = option_name
        if not opt.get_by_name():
            opt.type = option_type
            opt.acl_write = ["write-all"]
            opt.acl_read = ["read-all"]
            if option_value:
                opt.value = option_value
            if not opt.save():
                logging.error("Could not create option: %s" % option_name)
                return False
        return True


# End File: cver/src/migrate/data/data_options.py
