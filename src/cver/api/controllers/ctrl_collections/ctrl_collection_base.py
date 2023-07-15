"""
    Cver Api - Controller Collection
    Control Collection Base

"""


def get(collection) -> dict:
    """Base collections getter."""
    # args = api_util.get_params()
    data = {
        "status": "error",
        "message": "",
        "objects": [],
        "object_type": collection().collect_model.model_name
    }
    collect_data = collection().get_paginated()
    for obj in collect_data["objects"]:
        data["objects"].append(obj.json())
    data["info"] = collect_data["info"]
    data["status"] = "success"
    return data

# End File: cver/src/api/controllers/ctrl_collections/ctrl_collection_base.py
