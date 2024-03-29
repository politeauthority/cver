"""
    Cver Test - Unit
    Shared - Utils Xlate
    Tests File: cver/src/cver/shared/utils/xlate.py

"""
# import json
# from urllib.parse import unquote, quote, quote_plus

from pytest import raises

from cver.shared.utils import xlate


class TestSharedUtilsXlate:

    def test__url_decode(self):
        """
        :method: xlate.url_decode
        """
        assert xlate.url_decode("haproxy%3A2.0.12") == "haproxy:2.0.12"

    def test__url_encode(self):
        """
        :method: xlate.url_encode
        """
        assert xlate.url_encode("haproxy:2.0.12") == "haproxy%3A2.0.12"

    # def test__url_encode_json(self):
    #     data = {
    #         "simple": "dictionary"
    #     }
    #     result = xlate.url_encode_json(data)
    #     result = result.replace("+", " ")
    #     result = unquote(result)
    #     result = json.loads(result)
    #     assert isinstance(result, dict)
    #     assert data == result

    # def test__url_decode_json(self):
    #     """
    #     """
    #     data = {
    #         "simple": "dictionary"
    #     }
    #     encoded_data  = quote_plus(json.dumps(data))
    #     assert data =
    #     result = xlate.url_encode_json(data)

    def test__convert_any_to_int(self):
        """
        :method: xlate.convert_any_to_int
        """
        assert not xlate.convert_any_to_int(None)
        assert xlate.convert_any_to_int("1") == 1
        assert xlate.convert_any_to_int(5) == 5

    def test__convert_bool_to_int(self):
        """Test that bools are properly converted to ints, even when the input is a string value, to
        the best that we can.
        :method: xlate.convert_bool_to_int
        """
        assert xlate.convert_bool_to_int(True) == 1
        assert xlate.convert_bool_to_int(False) == 0
        assert xlate.convert_bool_to_int("True") == 1
        assert xlate.convert_bool_to_int("False") == 0
        assert not xlate.convert_bool_to_int("Falsy")

    def test__convert_int_to_bool(self):
        """
        :method: xlate.convert_int_to_bool
        """
        assert not xlate.convert_int_to_bool(None)
        assert xlate.convert_int_to_bool(1)
        assert xlate.convert_int_to_bool(0) == False

    def test__convert_list_to_str(self):
        """
        :method: xlate.convert_list_to_str
        """
        assert not xlate.convert_list_to_str([])
        # with raises(AttributeError):
        #     assert xlate.convert_list_to_str("hello")
        assert xlate.convert_list_to_str(["hello"])
        test_list = ["hello", "how", "are", "you"]
        assert xlate.convert_list_to_str(test_list) == "hello,how,are,you"

    def test__convert_str_to_bool(self):
        """
        :method: xlate.convert_str_to_bool
        """
        assert not xlate.convert_str_to_bool(None)
        assert xlate.convert_str_to_bool("true")
        assert xlate.convert_str_to_bool("1")
        assert xlate.convert_str_to_bool(1)
        assert not xlate.convert_str_to_bool("false")
        assert not xlate.convert_str_to_bool("0")
        assert not xlate.convert_str_to_bool(0)
        with raises(AttributeError):
            assert xlate.convert_str_to_bool("hello")

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

    def test__get_digest(self):
        """Test that we can convert snake case to camel case.
        :method: xlate.snake_to_camel_case()
        """
        expected = "d480d804f0c11548d6be95568"
        digest = "docker-pullable://docker.io/politeauthority/pignus@sha256:"
        digest += expected
        assert expected == xlate.get_digest(digest)

# End File: cver/tests/unit/shared/utils/test_xlate.py
