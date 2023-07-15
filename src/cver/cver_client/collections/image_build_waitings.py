"""
    Cver Client
    Collections - ImageBuildWaitings

"""
import importlib

from cver.shared.utils import xlate
from cver.shared.models.image_build_waiting import FIELD_MAP
from cver.cver_client.collections.client_collections_base import ClientCollectionsBase


class ImageBuildWaitings(ClientCollectionsBase):

    def __init__(self):
        """Create the instance."""
        super(ImageBuildWaitings, self).__init__()
        self.field_map = FIELD_MAP
        self.model_name = "image-build-waiting"
        self.collection_name = "image-build-waitings"

    def get(self):
        """Get a paginated list of entities."""
        response = self.make_request(self.collection_name)
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
        """Build """
        bare_model = self.dynamic_get_model_instance(object_type)
        print(bare_model)
        ret_list = []
        for obj in objs:
            thing = bare_model
            thing.build(obj)
            ret_list.append(thing)
        return ret_list

# End File: cver/src/cver_client/collections/image_build_waitings.py
