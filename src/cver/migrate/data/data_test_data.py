"""
    Cver Migrate
    Data - Test Data

"""
import logging

from cver.api.models.option import Option


class DataTestData:

    def create(self) -> bool:
        """Create the test data."""
        self.create_test_options()

    def create_test_options(self):
        """Build some Options that we can run tests against."""
        opt_str = Option()
        opt_str.type = "str"
        opt_str.name = "test_option_str"
        opt_str.get_by_name()
        opt_str.acl_write = ["write-all"]
        opt_str.acl_read = ["read-all"]
        opt_str.save()

        logging.info("Test Data: Options - create successful")

# End File: cver/src/migrate/data/data_test_data.py
