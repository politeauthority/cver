"""
    Cver Client
    Collections
    Base

"""
import importlib

from cver.shared.utils import xlate
from cver.cver_client import CverClient


class ClientCollectionsBase(CverClient):

    def __init__(self):
        super(ClientCollectionsBase, self).__init__()

    def get(self, args: dict = {}):
        """Get a paginated list of entities."""
        payload = {}
        if "search" in args:
            payload = {
                "search": xlate.url_encode_json(args["search"])
            }
        elif args:
            payload = self._prepare_search(args)

        response = self.make_request(self.collection_name, payload=payload)
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
        bare_model = self.dynamic_get_model_instance(object_type)
        print(bare_model)
        ret_list = []
        for obj in objs:
            thing = bare_model
            thing.build(obj)
            ret_list.append(thing)
        return ret_list

    def _prepare_search(self, args: dict) -> dict:
        """Prepare a search query for a collection."""
        search = {}
        for field_name, field_value in args.items():
            if field_name in self.field_map:
                if "api_searchable" not in self.field_map[field_name]:
                    continue
                if not self.field_map[field_name]["api_searchable"]:
                    continue
                search[field_name] = field_value
        return search


# End File: cver/src/cver_client/collections/client_connections_base.py
