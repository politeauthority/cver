"""
    Cver Test Regression
    CverClient - Model - Option
    Source: src/cver/cver_client/models/tasks.py

"""
from cver.client.models.option import Option


class TestCverClientModelOption:

    def test__get(self):
        """Test that we can get an Option
        """
        option = Option()
        assert option.get_by_name("engine_download_limit")
        assert option.name == "engine_download_limit"
        assert option.type == "int"

    def test__save(self):
        """Test that we can save an Option value."""
        option = Option()
        assert option.get_by_name("engine_download_limit")
        if option.value >= 1:
            new_value = option.value + 1
        else:
            new_value = option.value - 1

        option.value = new_value

        assert option.save()
        assert option.value == new_value

# End File: cver/tests/regression/cver_client/models/test_option.py
