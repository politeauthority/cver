"""
    Cver Api
    Controllers
    Collection Base

"""
import logging

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
    page = 1
    if "page" in request_args:
        page = request_args["page"]
    field_map = collection().collect_model().field_map
    where_and = _get_where_and(request_args["raw_args"], field_map)

    # Get the data
    collect_data = collection().get_paginated(page=page, where_and=where_and)
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


def _get_where_and(raw_args: dict, field_map: dict) -> list:
    """Gets the where_and value to be sent to collection paginationation search from the raw_args
    submitted in the requset
    """
    where_and = []
    if not raw_args:
        return []
    for raw_arg_field, raw_arg_data in raw_args.items():
        fn = raw_arg_field
        if fn not in field_map:
            logging.warning("Field %s not in %s" % (fn, "entity"))
            continue
        if "api_searchable" not in field_map[fn] or not field_map[fn]["api_searchable"]:
            logging.warning("Field %s not api searchable in %s" % (fn, "entity"))
            continue
        field_data = {}
        field_data["field"] = raw_arg_field

        if not isinstance(raw_arg_data, dict):
            field_data = {
                "field": raw_arg_field,
                "value": raw_arg_data,
                "op": "=",
            }
        else:
            field_data["value"] = raw_arg_data["value"]
            if "op" not in raw_arg_data or not raw_arg_data["op"]:
                field_data["op"] = "="
            else:
                field_data["op"] = raw_arg_data["op"]
        where_and.append(field_data)
    return where_and


def _get_object_type(collection) -> str:
    """Get an object name from the collection.
    :unit-test: TestCtrlCollectionBase.test___get_object_type
    """
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
