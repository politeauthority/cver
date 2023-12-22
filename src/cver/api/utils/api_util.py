"""
    Cver Api
    Api Utilities

"""
import logging
import json

from flask import request, make_response

from cver.shared.utils import xlate


def get_params() -> dict:
    """Extract the parameters from an api request.
    :unit-test: TestApiUtilApiUtil::test__get_params
    """
    ret_args = {
        "page": 1,
        "per_page": 20,
        "get_json": True,
        "get_api": True,
        "raw_args": {},
        "clean_args": {}
    }
    raw_args = request.args
    if "p" in raw_args and raw_args["p"].isdigit():
        ret_args["page"] = int(raw_args["p"])
    elif "page" in raw_args and raw_args["page"].isdigit():
        ret_args["page"] = int(raw_args["page"])

    if raw_args:
        ret_args["raw_args"]["query_str"] = raw_args
        ret_args["clean_args"]["fields"] = _get_search_field_args(raw_args)

    if "query" in raw_args:
        query = xlate.url_decode_json(raw_args["query"])
        ret_args["clean_args"]["fields"] = _post_search_field_args(query)
        ret_args["clean_args"]["order_by"] = _post_search_order_args(query)
        ret_args["clean_args"]["limit"] = _post_search_limit_args(query)

        return ret_args

    if not request.data:
        return ret_args
    # @todo: clean this part up, make a better response and handling
    try:
        request_data = request.get_json()
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"Recieved data that cant be decoded to JSON: {e}")
        return make_response("ERROR", 401)

    ret_args["raw_args"].update(request_data.items())
    _validate_args(raw_args)
    ret_args["clean_args"]["fields"] = _post_search_field_args(request_data)
    ret_args["clean_args"]["order_by"] = _post_search_order_args(request_data)
    ret_args["clean_args"]["limit"] = _post_search_limit_args(request_data)

    return ret_args


def _get_search_field_args(raw_args: dict) -> dict:
    """Get query paramaters from the url, mapping them as fields if they dont appear to be specific
    key words.
    :unit-test: TestApiUtilApiUtil::test___get_search_field_args
    """
    ret = {}
    if not raw_args:
        return ret
    non_model_fields = ["p", "page", "limit", "query"]
    for raw_key, raw_value in raw_args.items():
        if raw_key not in non_model_fields:
            ret[raw_key] = {
                "field": raw_key,
                "value": raw_value,
                "op": "="
            }
    return ret


def _post_search_field_args(the_args: dict) -> dict:
    """Extracts the field portion of a search query.
    :unit-test: TestApiUtilApiUtil::test___post_search_field_args
    """
    ret = {}
    if "fields" not in the_args:
        return ret
    for arg_key, arg_info in the_args["fields"].items():
        if isinstance(arg_info, str) or isinstance(arg_info, int):
            ret[arg_key] = {
                "field": arg_key,
                "value": arg_info,
                "op": "="
            }
        else:
            if "value" not in arg_info:
                logging.warning("No value argument in request")
                continue
            if "op" not in arg_info:
                operation = "="
            else:
                operation = arg_info["op"]
            ret[arg_key] = {
                "field": arg_key,
                "value": arg_info["value"],
                "op": operation
            }
    return ret


def _post_search_order_args(the_args: dict) -> dict:
    """Get search field arguments from a request.
    :unit-test: TestApiUtilApiUtil::test___post_search_order_args
    """
    if "order_by" not in the_args:
        return {}

    ret = {
        "field": the_args["order_by"]["field"],
        "direction": the_args["order_by"]["direction"]
    }
    return ret


def _post_search_limit_args(the_args: dict) -> dict:
    """Get limit arg from the request.
    :unit-test: TestApiUtilApiUtil::test___post_search_limit_args
    """
    if "limit" not in the_args:
        return None
    limit = the_args["limit"]
    if not isinstance(limit, int):
        return None
    return limit


def _validate_args(raw_args: dict):
    accepted_keys = ["fields", "limit", "order_by"]
    errors = []
    for raw_arg, arg_data in raw_args.items():
        if raw_args not in accepted_keys:
            errors.append("Arg: '%s' not allowed")

    if errors:
        data = {
            "status": "error",
            "message": ""
        }
        data["message"] = " ".join(errors)
        logging.warning("Client sent invalid search request: %s" % data["message"])
        return make_response(json.dumps(errors), 400)


# End File: cver/src/api/utils/api_util.py
