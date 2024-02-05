"""
    Utility Xlate
    Cver Shared
    A collection of misc trasnlation functions used all throuhout the Pignus platofrm.

    Testing:
        Unit test file  cver/tests/unit/shared/utils/test_xlate.py
        Unit tested     10/15

"""
import json
import logging
from urllib.parse import unquote, quote, quote_plus


def url_decode(encoded_str: str) -> str:
    """Decode a URL str such as "haproxy%3A2.0.12" to "haproxy:2.0.12"
    :unit-test: TestSharedUtilsXlate::test__url_decode
    """
    if not encoded_str:
        return ""
    return unquote(encoded_str)


def url_encode(slug: str) -> str:
    """Encode a str to be URL safe. Such as "haproxy:2.0.12" to "haproxy%3A2.0.12"
    :unit-test: TestSharedUtilsXlate::test__url_encode
    """
    butterfly = quote(slug)
    butterfly = butterfly.replace("/", "%2F")
    return butterfly


def url_encode_json(data: dict) -> str:
    """Ecode a dict into JSON, primarily used for collection search term requests."""
    json_dump = json.dumps(data)
    return quote_plus(json.dumps(json_dump))


def url_decode_json_flask(encoded_str: str) -> dict:
    """This is not the write name for this
    """
    if not encoded_str:
        return {}
    # Remove the outer double quotes
    input_str = encoded_str.strip('"')

    # Replace double-escaped double quotes with regular double quotes
    input_str = input_str.replace('\\"', '"')

    # Unescape single-escaped single quotes with regular single quotes
    input_str = input_str.replace("\\'", "'")

    try:
        # Parse the string as JSON into a Python dictionary
        output_dict = json.loads(input_str)
        return output_dict
    except json.decoder.JSONDecodeError as e:
        logging.warning("Cant parse json: %s\nInput Data:\n %s\nParsed Data:\n%s" % (
            e,
            encoded_str,
            input_str))
        return {}
    # Print the resulting dictionary
    return output_dict
    input_str = encoded_str.strip('"')
    input_str = input_str.replace('\\"', '"')
    try:
        output_dict = json.loads(input_str)
        return output_dict
    except json.decoder.JSONDecodeError as e:
        logging.warning("Cant parse json: %s\nInput Data:\n %s\nParsed Data:\n%s" % (
            e,
            encoded_str,
            input_str))
        return {}


def url_decode_json(encoded_str: str) -> dict:
    decoded_str = url_decode(encoded_str)
    decoded_str = decoded_str.strip('"')
    decoded_str = decoded_str.rstrip('"')
    decoded_str = decoded_str.replace("+", " ")
    decoded_str = decoded_str.replace('\\"', '"')
    decoded_str = decoded_str.strip('"')
    decoded_str = decoded_str.rstrip('""')
    decoded_str = decoded_str.rstrip('"\\')
    try:
        # Parse the string as JSON into a Python dictionary
        output_dict = json.loads(decoded_str)
        return output_dict
    except json.decoder.JSONDecodeError as e:
        logging.warning("Cant parse json: %s\nInput Data:\n %s\nParsed Data:\n%s" % (
            e,
            encoded_str,
            decoded_str))
        return {}


def convert_any_to_int(value) -> int:
    """Attempt to convert any value into an int
    :unit-test: TestXlate::test__convert_any_to_int
    """
    if not value:
        return None
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, int):
        return value
    else:
        try:
            if value.isdigit():
                return int(value)
            else:
                raise AttributeError(
                    'Cannot convert "%s" of type "%s" to int.' % (
                        value,
                        type(value)))
        except AttributeError as e:
            raise AttributeError(
                'Cannot convert "%s" of type "%s" to int. Exception: %s' % (
                    value,
                    type(value),
                    e))


def convert_bool_to_int(value: bool) -> int:
    """Convert a bool into an int. Typically used for storing bools as TINYINT in SQL.
    @todo: This should probably rasie an Attribute error with bad string input.
    :unit-test: TestXlate::test__convert_bool_to_int
    """
    if isinstance(value, type(None)):
        return None
    elif value:
        if isinstance(value, str):
            value = value.lower()
            if value == "true":
                return 1
            elif value == "false":
                return 0
            else:
                logging.error("Cannot convert str: %s to bool" % value)
                return None
        return 1
    elif not value:
        return 0
    else:
        msg = 'Cannot convert "%s" of type "%s" to int' % (value, type(value))
        raise AttributeError(msg)


def convert_int_to_bool(value: int) -> bool:
    """Convert an into into a bool. Typically used for pulling TINYINT values out of a SQL
    database and converting it into a python bool
    :unit-test: TestXlate::test__convert_int_to_bool
    """
    if isinstance(value, type(None)):
        return None
    elif value == 1:
        return True
    elif value == 0:
        return False


def convert_str_to_bool(value: str) -> bool:
    """Convert a string value to a bool value if one can be derrived.
    :unit-test: TestXlate::test__convert_str_to_bool
    """
    if not value:
        return None
    if isinstance(value, bool):
        return value
    value = str(value)
    value = value.lower().strip()
    accepted_true_values = ["true", "1", 1]
    accepted_false_values = ["false", "0", 0]

    if value in accepted_true_values:
        return True
    elif value in accepted_false_values:
        return False
    raise AttributeError(
        'Cannot convert "%s" of type "%s" to bool.' % (
            value,
            type(value)))


def convert_any_to_bool(value: str) -> bool:
    """Attempt to convert any data into a bool
    :unit-test: TestXlate::test__convert_any_to_bool
    """
    if not value:
        return False
    if isinstance(value, bool):
        return value
    elif isinstance(value, str):
        return convert_str_to_bool(value)
    elif isinstance(value, int()):
        return convert_int_to_bool(value)
        return value
    else:
        raise AttributeError(
            'Cannot convert "%s" of type "%s" to bool.' % (
                value,
                type(value)))


def convert_list_to_str(value: list) -> str:
    """Convert a list into a str. Typically used for storing lists as a TEXT field in SQL.
    :unit-test: TestXlate::test__convert_bool_to_int
    """
    if not value:
        return None
    if isinstance(value, str):
        value = [value]

    clean_values = []
    for item in value:
        clean_values.append(str(item))

    return ",".join(clean_values)


def get_digest(image_str: str):
    """Extracts the digest from a docker-pullable string as given from the K8 api
    example image_str: docker-pullable://docker.io/politeauthority/pignus@sha256:\
        d480d804f0c11548d6be95568
    :unit-test: TestXlate::test__get_digest
    """
    return image_str[image_str.find("@sha256:") + 8:]


def json_dump(the_dict: dict) -> str:
    """Create a JSON safe str from native Python objects, recursively iterating over a dictionary
    and converting those that would normally break into their str representation.
    :unit-test: TestXlate::test__json_dump()
    """
    new_json = _convert_dict_objects(the_dict)
    return json.dumps(new_json)


def _convert_dict_objects(the_dict):
    """Recursily scrubs non serializable objects from a dictionary replacing them with their str
    represntations.
    """
    new_dict = {}
    for key, value in the_dict.items():
        if _is_jsonable(value, exclude_dicts=True):
            new_dict[key] = value
        elif isinstance(value, dict):
            new_dict[key] = _convert_dict_objects(value)
        else:
            new_dict[key] = str(value)
    return new_dict


def _is_jsonable(item, exclude_dicts: bool = False) -> bool:
    """Tests to see if a given value is JSONable.
    """
    jsonable = ["str", "bool", "int", "float"]
    if not exclude_dicts:
        jsonable.append("dict")
    if type(item).__name__ in jsonable:
        return True
    else:
        return False


def rest_to_snake_case(rest: str) -> str:
    """Convert rest case to snake case, ie - to _
    Centralizing this as it's a common operatorion.
    :unit-test: test__rest_to_snake_case
    """
    return rest.replace("-", "_")


def snake_to_camel_case(snake: str) -> str:
    """Turn snake case into camel case.
    example in: some_thing_long
    example out: SomeThingLong
    :unit-test: test__snake_to_camel_case
    """
    if not snake:
        return ""
    if "_" not in snake:
        camel = "%s%s" % (snake[0].upper(), snake[1:])
        return camel

    indices = []
    index = snake.find("_")
    while index != -1:
        indices.append(index)
        index = snake.find("_", index + 1)
    camel = snake
    camel = ""
    last_indi = 0
    for indi in indices:
        capitol = last_indi
        if capitol == 0:
            capitol = 0
        else:
            capitol = last_indi + 1
        camel += "%s%s" % (snake[capitol].upper(), snake[capitol + 1:indi])
        last_indi = indi

    camel += snake[last_indi:]
    if "_" in camel:
        pos = camel.find("_")
        camel = camel.replace("_", "")
        camel = camel[:pos] + camel[pos].upper() + camel[pos + 1:]
    return camel

# End File: cver/src/cver/shared/utils/xlate.py
