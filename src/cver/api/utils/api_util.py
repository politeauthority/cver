"""
    Cver Api
    Api Utilities

"""
import logging
import json

from flask import request, make_response


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

    for arg_key, arg_value in request.args.items():
        if arg_key != "p":
            ret_args["raw_args"][arg_key] = {
                "field": arg_key,
                "value": arg_value,
                "op": "="
            }
    for key, item in raw_args.items():
        if key not in ret_args["raw_args"]:
            ret_args["raw_args"][key] = item

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
    ret_args["clean_args"]["fields"] = _get_search_field_args(request_data)
    ret_args["clean_args"]["order_by"] = _get_search_order_args(request_data)
    # for field, args in request_data.items():
    #     ret_args["raw_args"][field] = {}
    #     ret_args["raw_args"][field]["field"] = field
    #     ret_args["raw_args"][field]["value"] = args["value"]
    #     if "op" not in args or not args["op"]:
    #         ret_args["raw_args"][field]["op"] = "="
    #     else:
    #         ret_args["raw_args"][field]["op"] = args["op"]

    return ret_args


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


def _get_search_field_args(the_args: dict) -> dict:
    """
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


def _get_search_order_args(the_args: dict) -> dict:
    """
    """
    ret = {}
    if "order_by" not in the_args:
        return ret

    ret = {
        "field": the_args["order_by"]["field"],
        "direction": the_args["order_by"]["direction"]
    }
    return ret

# End File: cver/src/api/utils/api_util.py
