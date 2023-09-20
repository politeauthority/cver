"""
    Api Utilities

"""

from flask import request


def get_params() -> dict:
    args = {
        "page": 1,
        "per_page": 20,
        "get_json": True,
        "get_api": True,
        "raw_args": {}
    }
    raw_args = request.args
    if "p" in raw_args and raw_args["p"].isdigit():
        args["page"] = int(raw_args["p"])

    for arg_key, arg_value in request.args.items():
        if arg_key != "p":
            args["raw_args"][arg_key] = arg_value

    return args

# End File: cver/src/api/utils/api_util.py
