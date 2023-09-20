"""
    Cver Api - Controller Collection
    Control Collection Base

"""
from cver.api.utils import api_util


def get(collection) -> dict:
    """Base collections getter."""
    request_args = api_util.get_params()
    data = {
        "status": "error",
        "message": "",
        "objects": [],
        "object_type": _get_object_type(collection)
    }
    field_map = collection().collect_model().field_map
    where_and = []
    if request_args["raw_args"]:
        for raw_arg_field, raw_arg_value in request_args["raw_args"].items():
            if raw_arg_field in field_map and field_map[raw_arg_field]["api_searchable"]:
                where = {
                    "field": raw_arg_field,
                    "value": raw_arg_value,
                    "op": "="
                }
                where_and.append(where)
    collect_data = collection().get_paginated(where_and=where_and)
    for obj in collect_data["objects"]:
        data["objects"].append(obj.json())

    # Fuzz out data we wont show on the api keys
    hidden_fields = _get_api_hidden_fields(field_map)
    if hidden_fields:
        c = 0
        for obj in data["objects"]:
            for hiden_field in hidden_fields:
                data["objects"][c][hiden_field] = "hidden"
            c += 1

    data["info"] = collect_data["info"]
    data["status"] = "success"
    return data


def _get_object_type(collection) -> str:
    object_type = collection().collect_model.model_name
    if "_" in object_type:
        object_type = object_type.replace("_", "-")
    return object_type


def _get_api_hidden_fields(field_map: dict) -> list:
    hidden_fields = []
    for field_name, field_info in field_map.items():
        if "api_display" in field_info and field_info["api_display"] == False:
            hidden_fields.append(field_name)
    return hidden_fields

# End File: cver/src/api/controllers/ctrl_collections/ctrl_collection_base.py
