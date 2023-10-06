"""
    Api Utilities

"""

from flask import request


def get_params() -> dict:
    ret_args = {
        "page": 1,
        "per_page": 20,
        "get_json": True,
        "get_api": True,
        "raw_args": {}
    }
    raw_args = request.args
    if "p" in raw_args and raw_args["p"].isdigit():
        ret_args["page"] = int(raw_args["p"])
    elif "page" in raw_args and raw_args["page"].isdigit():
        ret_args["page"] = int(raw_args["page"])

    for arg_key, arg_value in request.args.items():
        if arg_key != "p":
            ret_args["raw_args"][arg_key] = arg_value
    return ret_args

# End File: cver/src/api/utils/api_util.py
