"""
    Api Utilities

"""
import logging
import json

from flask import request, make_response


def get_params() -> dict:
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
    if not request.data:
        return ret_args
    # @todo: clean this part up, make a better response and handling
    try:
        request_data = request.get_json()
    except json.decoder.JSONDecodeError as e:
        logging.warning(f"Recieved data that cant be decoded to JSON: {e}")
        return make_response("ERROR", 401)

    ret_args["raw_args"].update(request_data.items())
    # for field, args in request_data.items():
    #     ret_args["raw_args"][field] = {}
    #     ret_args["raw_args"][field]["field"] = field
    #     ret_args["raw_args"][field]["value"] = args["value"]
    #     if "op" not in args or not args["op"]:
    #         ret_args["raw_args"][field]["op"] = "="
    #     else:
    #         ret_args["raw_args"][field]["op"] = args["op"]

    return ret_args

# End File: cver/src/api/utils/api_util.py
