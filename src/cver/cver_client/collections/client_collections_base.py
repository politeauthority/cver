"""
    Cver Client
    Collections
    Base

"""
import logging

from cver.shared.utils import xlate
from cver.cver_client import CverClient
from cver.cver_client.utils import misc


class ClientCollectionsBase(CverClient):

    def __init__(self):
        super(ClientCollectionsBase, self).__init__()
        self.field_map = {}
        self.model = None
        self.collection_name = None
        self.response_last = None

    def get(self, request_args: dict = {}, page: int = 1) -> list:
        """Get a paginated list of entities."""
        payload = {}
        payload["page"] = page
        query_stmt = False
        if "query" in request_args:
            query_stmt = True
        if query_stmt:
            payload = {
                "query": xlate.url_encode_json(request_args)
            }
        elif request_args:
            payload = self._prepare_search(request_args)
        response = self.make_request(self.collection_name, payload=payload)
        self.response_last = response
        if response["status"] == "success":
            return self.build_list_of_dicts(response["object_type"], response["objects"])
        else:
            return False

    def build_list_of_dicts(self, object_type: str, objs: list) -> list:
        """Builds a list of dictionaries."""
        # bare_model = self.dynamic_get_model_instance(object_type)
        ret_list = []
        for obj in objs:
            thing = misc.dynamic_get_model_instance(object_type)
            thing.build(obj)
            ret_list.append(thing)
            thing = None
        return ret_list

    def _prepare_search(self, args: dict) -> dict:
        """Prepare a search query for a collection.
        :return:
            example:
                {
                    "fields": {
                        "waiting_for": {
                            "value": "scan"
                        },
                        "fail_count": {
                            "op": "lt",
                            "value": 1
                        }
                    },
                    "order_by": {
                        "field": "id",
                        "direction": "ASC"
                    },
                    "limit": 5
                }
        """
        return args
        payload = {}
        accepted_keys = ["fields", "order_by", "limit"]
        for arg_key, arg_value in args.items():
            if arg_key not in accepted_keys:
                logging.error("Key %s is not valid" % arg_key)
                continue
            if arg_key == "fields":
                if "fields" not in payload:
                    payload["fields"] = {}
                for field_name, field_query in arg_value.items():
                    if field_name in self.field_map:
                        if "api_searchable" not in self.field_map[field_name]:
                            continue
                        if not self.field_map[field_name]["api_searchable"]:
                            continue
                        if isinstance(field_query, str):
                            payload["fields"][field_name] = field_query
                        elif isinstance(field_query, dict):
                            payload["fields"][field_name] = field_query
            elif arg_key == "order_by":
                payload["order_by"] = args["order_by"]
            elif arg_key == "limit":
                payload["limit"] = args["limit"]
        # logging.debug("\nPARDED PAYLOAD:\n\t%s" % payload)
        return payload


# End File: cver/src/cver_client/collections/client_connections_base.py
