"""
    Cver Client
    Collections
    Base

"""
import importlib
import logging

from cver.shared.utils import xlate
from cver.cver_client import CverClient


class ClientCollectionsBase(CverClient):

    def __init__(self):
        super(ClientCollectionsBase, self).__init__()
        self.field_map = {}
        self.model = None
        self.collection_name = None
        self.response_last = None

    def get(self, args: dict = {}, page: int = 1) -> list:
        """Get a paginated list of entities."""
        payload = {}
        payload["page"] = page
        if "search" in args:
            payload = {
                "search": xlate.url_encode_json(args["search"])
            }
        elif args:
            payload = self._prepare_search(args)
        print("PAYLOAD: %s" % payload)
        response = self.make_request(self.collection_name, payload=payload)
        self.response_last = response
        if response["status"] == "success":
            return self.build_list_of_dicts(response["object_type"], response["objects"])
        else:
            return False

    def dynamic_get_model_instance(self, object_type: str):
        """Dynamically get a model instance. We dont know the model we need at run time so we need
        to import it dynamically.
        @todo: This should be tested and made more clear.
        """
        snake_str = xlate.rest_to_snake_case(object_type)
        camel_str = xlate.snake_to_camel_case(snake_str)
        module_path = "cver.cver_client.models.%s.%s" % (snake_str, camel_str)
        module_path = "cver.cver_client.models.%s" % (snake_str)
        module_file = importlib.import_module(module_path)
        module = getattr(module_file, camel_str)
        return module()

    def build_list_of_dicts(self, object_type: str, objs: list) -> list:
        """Builds a list of dictionaries."""
        # bare_model = self.dynamic_get_model_instance(object_type)
        ret_list = []
        for obj in objs:
            thing = self.dynamic_get_model_instance(object_type)
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
        payload = {}
        for arg_key, arg_value in args.items():
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
        logging.debug("\nPARDED PAYLOAD:\n\t%s" % payload)
        return payload


# End File: cver/src/cver_client/collections/client_connections_base.py
