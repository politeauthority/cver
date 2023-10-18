"""
    Cver Api
    Controllers
    Collection Base

"""
import logging

from cver.api.utils import api_util
from cver.shared.utils import xlate


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
    logging.info("\nREQUEST ARGS:\n%s" % request_args)
    if "page" in request_args:
        page = request_args["page"]
    field_map = collection().collect_model().field_map
    parsed_body = _parse_body(request_args["raw_args"], field_map)
    logging.info("\nRaw Args:\n%s" % request_args["raw_args"])
    logging.info("\nGET:\n%s" % parsed_body)
    # Get the data
    collect_data = collection().get_paginated(
        page=page,
        where_and=parsed_body["where_and"],
        order_by=parsed_body["order_by"]
    )
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


def _parse_body(raw_args: dict, field_map: dict) -> dict:
    """Gets the where_and value to be sent to collection paginationation search from the raw_args
    submitted in the requset
    :param raw_args: Raw arguments coming in from the api body request
        example:
            {
                "fields": {
                    "cve_high_int": {
                        "op": "gt",
                        "value": 1
                    }
                },
                "order_by": {
                    "field": "id",
                    "direction": "ASC"
                },
                "limit": 5
            }
    :unit-test: TestCtrlCollectionBase.test___parse_body
    """
    ret = {
        "where_and": [],
        "order_by": None,
        "limit": None,
        "page": None
    }
    if not raw_args:
        return ret

    for raw_arg_key, raw_arg_data in raw_args.items():
        if raw_arg_key == "fields":
            ret["where_and"] = _get_fields(raw_arg_data, field_map)
        elif raw_arg_key == "order_by":
            ret["order_by"] = _get_order_by(raw_arg_data)
            if not isinstance(raw_arg_data, dict):
                logging.warning("order_by is not string, dropping.")
                continue
            ret["order_by"] = raw_arg_data
        elif raw_arg_key == "limit":
            if not isinstance(raw_arg_data, int):
                logging.warning("limit is not int, dropping.")
                continue
            ret["limit"] = raw_arg_data

    return ret


def _get_object_type(collection) -> str:
    """Get an object name from the collection.
    :unit-test: TestCtrlCollectionBase.test___get_object_type
    """
    object_type = collection().collect_model.model_name
    if "_" in object_type:
        object_type = object_type.replace("_", "-")
    return object_type


def _get_api_hidden_fields(field_map: dict) -> list:
    """Get all fields that are not supposed to be displayed on the api.
    :unit-test: TestCtrlCollectionBase.test___get_api_hidden_fields
    """
    hidden_fields = []
    for field_name, field_info in field_map.items():
        if "api_display" in field_info and field_info["api_display"] == False:
            hidden_fields.append(field_name)
    return hidden_fields


def _get_fields(field_data: dict, field_map: dict) -> list:
    """Extract fields from the api request.

    :returns:
        example: [
            {
                "field": "created_ts",
                "value": "2023-10-13 01:00:00",
                "op": ">"
            }
        ]
    :unit-test: TestCtrlCollectionBase.test___get_fields
    """
    where_and_fields = []
    for fn, query_data in field_data.items():

        field_queryable = _field_queryable(fn, field_map)
        if not field_queryable:
            continue

        field_data = {
            "field": fn,
            "value": None,
            "op": None
        }

        # If the field is a direct query, ie {"name": "hello-world"}
        if not isinstance(query_data, dict):
            field_data = _query_direct(fn, query_data, field_map[fn])
            where_and_fields.append(field_data)
            continue

        else:
            field_data["value"] = query_data["value"]
            if "op" not in query_data or not query_data["op"]:
                print("no hit")
                field_data["op"] = "="
            else:
                print("we hit the get operation")
                field_data["op"] = _get_operation(query_data, field_map[fn])

        where_and_fields.append(field_data)
    return where_and_fields


def _get_order_by(order_data: dict) -> dict:
    """Extract order by from the api request.

    :returns:
        example:
            {
                "field": "id",
                "direction": "ASC"
            }
    :unit-test: TestCtrlCollectionBase.test___get_order_by
    """
    if not order_data:
        return {}
    for key, value in order_data.items():
        if key not in ["field", "direction"]:
            # @todo: add logging
            return {}
    return {
        "field": order_data["field"],
        "direction": order_data["direction"],
    }


def _field_queryable(field_name: str, field_map: dict) -> bool:
    """Determines if the field being queried, is allowed to be queried.
    :unit-test: TestCtrlCollectionBase::test___field_queryable
    """
    if field_name not in field_map:
        logging.warning("Field %s not in %s" % (field_name, "entity"))
        return False
    if "api_searchable" not in field_map[field_name]:
        logging.warning("Field %s not api searchable in %s" % (field_name, "entity"))
        False
    if not field_map[field_name]["api_searchable"]:
        logging.warning("Field %s not api searchable in %s" % (field_name, "entity"))
        return False
    return True


def _query_direct(field_name: str, query_data: str, field_map_field: dict) -> dict:
    """When a query comes in with a direct key to value relationship assume we want to do an =
    operation. {"name": "hello-world"}
    :unit-test: TestCtrlCollectionBase::test___query_direct
    """
    field_data = {
        "field": field_name,
        "value": query_data,
        "op": "=",
    }
    if field_map_field["type"] == "bool":
        field_data["value"] = xlate.convert_str_to_bool(field_data["value"])
        logging.debug("modified value to bool")
    return field_data


def _get_operation(query_data: dict, field_map_field: dict) -> str:
    """Get the operation for a single field.
    :unit-test: TestCtrlCollectionBase.test___get_operation
    """
    if "op" not in query_data:
        logging.warning("Operation not in query replacing with =")
        return "="
    if not isinstance(query_data["op"], str):
        logging.warning("Operation query is not string, replacing with =")
        return "="
    if query_data["op"].lower() not in ["=", ">", "<", "like", "gt", "lt"]:
        logging.error(
            'Unknown operation "%s" will be ignored and replaced with =' % (
                query_data["op"]))
        return "="
    if query_data["op"].lower() == "gt":
        operation = ">"
    elif query_data["op"].lower() == "lt":
        operation = "<"
    else:
        operation = query_data["op"].lower()
    if operation in ["<", ">"]:
        if field_map_field["type"] not in ["datetime", "int"]:
            msg = "Field: %s can not to greater than less than query, only datetime and int. "
            msg += "Replacing with ="
            msg = msg % field_map_field["name"]
            logging.warning(msg)
            operation = "="
    return operation

# End File: cver/src/api/controllers/ctrl_collections/ctrl_collection_base.py
