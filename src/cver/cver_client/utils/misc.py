"""
    Cver Client
    Utils
    Misc

"""
import importlib
from cver.shared.utils import xlate


def dynamic_get_model_instance(object_type: str):
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
