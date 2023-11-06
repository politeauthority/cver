"""
    Cver Test Regression
    CverClient - Model - Option
    Source: src/cver/cver_client/models/tasks.py

"""
from cver.client.models.option import Option


class TestCverClientModelOption:

    def test__get(self):
        """
        """
        option = Option()
        assert option.get_by_name("test_option_str")

    def test__save(self):
        """
        """
        option = Option()
        assert option.get_by_name("test_option_str")
        option.value = "new-value"
        assert option.save()
        assert option.value == "new-value"

# End File: cver/tests/regression/cver_client/models/test_option.py
