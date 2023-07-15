"""
    Cver Test - Unit
    Shared - Utils Xlate
    Tests File: cver/src/cver/shared/utils/xlate.py

"""
from cver.shared.utils import xlate


class TestSharedUtilsXlate:

    def test__rest_to_snake_case(self):
        """Test that we can convert rest case to snake case.
        :method: xlate.rest_to_snake_case()
        """
        assert xlate.rest_to_snake_case("module") == "module"
        assert xlate.rest_to_snake_case("my-module-is-great") == "my_module_is_great"

    def test__snake_to_camel_case(self):
        """Test that we can convert snake case to camel case.
        :method: xlate.snake_to_camel_case()
        """
        assert xlate.snake_to_camel_case("module") == "Module"
        assert xlate.snake_to_camel_case("my_module_is_great") == "MyModuleIsGreat"
        assert xlate.snake_to_camel_case("image_build_waiting") == "ImageBuildWaiting"


# End File: cver/tests/unit/shared/utils/test_xlate.py
